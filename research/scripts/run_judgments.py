"""Execute the existing blinded local-pilot queue, sequentially and resumably."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import perf_counter

from filelock import FileLock
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_openai_judge import read_key, redact, request_body
from experiment.judge_prompt import build_llm_judge_prompt
from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.judge_record import (JudgeExecutionRecord, JudgeConfiguration, JudgePromptSnapshot,
                                     CandidateResponseSnapshot, JudgeRuntimeMetadata, JudgeAttemptError)
from experiment.judge_response import parse_llm_judge_response, JudgeResponseValidationError
from experiment.pilot_runner import _append, _hash


def load_plan(directory):
    paths = {name: directory / name for name in ("judge_queue.jsonl", "judge_mapping.jsonl", "generations.jsonl")}
    queue = [json.loads(line) for line in paths["judge_queue.jsonl"].read_text(encoding="utf-8").splitlines()]
    mapping_rows = [json.loads(line) for line in paths["judge_mapping.jsonl"].read_text(encoding="utf-8").splitlines()]
    mapping = {r["evaluation_id"]: r for r in mapping_rows}
    events = [json.loads(line) for line in paths["generations.jsonl"].read_text(encoding="utf-8").splitlines()]
    header = events[0]
    if header["simulated"] or header["config_hash"] != _hash(header["config"]):
        raise ValueError("invalid or simulated generation source")
    config = json.loads((ROOT / "experiments/judge_model_selection.v1.json").read_text(encoding="utf-8"))["judge_configuration"]
    if config["model"] != header["config"]["judge"]["model"]:
        raise ValueError("judge configuration mismatch")
    schema = json.loads((ROOT / "experiments/llm_judge_response.schema.json").read_text(encoding="utf-8"))
    jobs = {j["job_id"]: j for j in header["jobs"]}
    results = {e["job_id"]: e for e in events[1:] if e["event"] == "result"}
    if len(queue) != 81 or len(mapping_rows) != 81 or len(mapping) != 81 or len({q["evaluation_id"] for q in queue}) != 81:
        raise ValueError("expected 81 unique judgments")
    if set(mapping) != {q["evaluation_id"] for q in queue}:
        raise ValueError("queue mapping mismatch")
    coverage = set()
    for row in queue:
        link = mapping[row["evaluation_id"]]
        job = jobs[link["job_id"]]
        result = results[job["job_id"]]
        payload = LessonPlanSemanticPayload.model_validate(job["payload"])
        text = result["response"]["content"]
        prompt = build_llm_judge_prompt(row["evaluation_id"], payload, text)
        if (result["status"] != "success" or row["prompt"] != prompt.text or row["prompt_sha256"] != prompt.sha256
                or row["prompt_version"] != prompt.template_version or link["payload_sha256"] != payload.semantic_hash
                or link["content_sha256"] != sha256(text.encode()).hexdigest()):
            raise ValueError("queue evidence mismatch")
        pair = (job["job_id"], link["judge_repetition"])
        if pair in coverage or link["judge_repetition"] not in (1, 2, 3):
            raise ValueError("duplicate or invalid judgment repetition")
        coverage.add(pair)
    if coverage != {(job_id, rep) for job_id in jobs for rep in (1, 2, 3)}:
        raise ValueError("incomplete judgment coverage")
    plan = {"event": "plan", "configuration": config, "schema": schema,
            "source_hashes": {name: sha256(path.read_bytes()).hexdigest() for name, path in paths.items()},
            "planned": 81, "automatic_retries": 0,
            "requests": [{"evaluation_id": row["evaluation_id"], "body": request_body(config, row["prompt"], schema)} for row in queue]}
    return plan, queue, mapping, jobs, results


def execute(directory, key, *, post=None, max_jobs=None):
    plan, queue, mapping, jobs, results = load_plan(directory)
    post = post or requests.post
    path = directory / "judgments.jsonl"
    with FileLock(str(path) + ".lock", timeout=0):
        events = []
        if path.exists():
            raw = path.read_text(encoding="utf-8")
            if not raw.endswith("\n"):
                raise ValueError("incomplete judgment log")
            events = [json.loads(line) for line in raw.splitlines()]
            if events[0] != plan:
                raise ValueError("judgment plan changed")
        started, finished = set(), {}
        allowed = {q["evaluation_id"] for q in queue}
        for event in events[1:]:
            eid = event["evaluation_id"]
            if eid not in allowed:
                raise ValueError("unknown judgment")
            if event["event"] == "started" and eid not in started:
                started.add(eid)
            elif event["event"] == "result" and eid in started and eid not in finished:
                finished[eid] = event
            else:
                raise ValueError("duplicate or invalid judgment event")
        if started - finished.keys():
            raise ValueError("unresolved started judgment; no automatic duplicate")
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            if not events:
                _append(stream, plan)
            count = 0
            for row, request in zip(queue, plan["requests"]):
                eid = row["evaluation_id"]
                if eid in finished:
                    continue
                if max_jobs is not None and count >= max_jobs:
                    break
                now = lambda: datetime.now(timezone.utc).isoformat()
                _append(stream, {"event": "started", "evaluation_id": eid, "at": now()})
                event = {"event": "result", "evaluation_id": eid, "status": "transport_error",
                         "http_status": None, "raw_response": None, "raw_text": None, "record": None, "error": None}
                start = perf_counter()
                try:
                    response = post("https://api.openai.com/v1/responses", headers={"Authorization": "Bearer " + key},
                                    json=request["body"], timeout=90)
                    event.update(http_status=response.status_code, request_id=response.headers.get("x-request-id"),
                                 raw_response=redact(response.json(), key))
                    raw = event["raw_response"]
                    if not response.ok:
                        event.update(status="api_error", error=raw.get("error"))
                    elif raw.get("model") != plan["configuration"]["model"]:
                        event.update(status="model_mismatch")
                    elif raw.get("status") != "completed":
                        event.update(status="incomplete_response")
                    else:
                        text = "".join(c["text"] for item in raw.get("output", [])
                                       for c in item.get("content", []) if c.get("type") == "output_text")
                        event["raw_text"] = text
                        validated, error = None, None
                        try:
                            validated = parse_llm_judge_response(text, eid)
                        except JudgeResponseValidationError as failure:
                            error = JudgeAttemptError.from_validation_error(failure)
                        link = mapping[eid]
                        job = jobs[link["job_id"]]
                        candidate = results[job["job_id"]]["response"]["content"]
                        payload = LessonPlanSemanticPayload.model_validate(job["payload"])
                        usage = raw.get("usage") or {}
                        record = JudgeExecutionRecord(
                            record_id=eid + "-a1", evaluation_id=eid, task_id=job["task_id"], condition=job["condition"],
                            generation_execution_id=job["job_id"], repetition=link["judge_repetition"],
                            status="error" if error else "success",
                            prompt=JudgePromptSnapshot.from_artifact(build_llm_judge_prompt(eid, payload, candidate)),
                            candidate=CandidateResponseSnapshot.from_text(candidate),
                            judge_configuration=JudgeConfiguration(**plan["configuration"]), raw_response=text,
                            validated_response=validated, error=error,
                            runtime=JudgeRuntimeMetadata(latency_ms=(perf_counter() - start) * 1000,
                                input_tokens=usage.get("input_tokens"), output_tokens=usage.get("output_tokens"),
                                finish_reason=raw.get("status"), raw_metadata={"response_id": raw.get("id"),
                                    "model": raw.get("model"), "service_tier": raw.get("service_tier")}))
                        event.update(status="validation_error" if error else "success", record=record.model_dump(mode="json"))
                except (requests.RequestException, ValueError) as failure:
                    event["error"] = {"type": type(failure).__name__}
                event.update(latency_ms=(perf_counter() - start) * 1000, at=now())
                _append(stream, redact(event, key))
                finished[eid] = event
                count += 1
                print(json.dumps({"completed": len(finished), "planned": 81, "last_status": event["status"]}), flush=True)
                if event["http_status"] in (401, 403, 404, 429):
                    break
    return {"completed": len(finished), "success": sum(e["status"] == "success" for e in finished.values()), "planned": 81}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if args.live:
        key = read_key()
        if not key:
            raise SystemExit("OpenAI credential absent")
        print(json.dumps(execute(args.directory, key)))
    else:
        plan, *_ = load_plan(args.directory)
        print(json.dumps({"validated_plan": True, "planned": plan["planned"], "api_calls": 0}))
