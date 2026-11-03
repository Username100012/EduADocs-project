"""Package v2 judgments from saved responses offline; no execution or billing."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.judge_contract_v2 import build_prompt, response_schema, PROMPT_VERSION
from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.pilot_runner import _hash
from check_openai_judge import request_body
from evaluate_pilot import evaluate


def prepare(source, output, *, configuration=None):
    config = configuration
    if config is None:
        header = json.loads((source / "generations.jsonl").read_text(encoding="utf-8").splitlines()[0])
        config = header["config"] if header["config"].get("study_phase") == "main" else json.loads(
            (ROOT / "experiments/main_config.json").read_text(encoding="utf-8"))
    contract = config["judge"]["contract"]
    for name, expected in contract["artifact_sha256"].items():
        if sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("closed contract changed")
    log = source / "generations.jsonl"
    events = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    metrics = evaluate(log, version="v2")  # Reuse log sequencing/config validation.
    jobs = {j["job_id"]: j for j in events[0]["jobs"]}
    queue, mapping = [], []
    source_hash = sha256(log.read_bytes()).hexdigest()
    config_hash = _hash(config)
    for event in events[1:]:
        if event["event"] != "result" or event["status"] != "success":
            continue
        job = jobs[event["job_id"]]
        candidate = event["response"]["content"]
        payload = LessonPlanSemanticPayload.model_validate(job["payload"])
        for repetition in range(1, config["judge"]["repetitions_per_response"] + 1):
            eid = "eval-" + _hash([PROMPT_VERSION, source_hash, job["job_id"], repetition, config_hash])[:32]
            prompt = build_prompt(eid, payload, candidate)
            queue.append({"evaluation_id": eid, "prompt": prompt.text, "prompt_sha256": prompt.sha256,
                          "body": request_body(config["judge"]["configuration"], prompt.text, response_schema())})
            mapping.append({"evaluation_id": eid, "job_id": job["job_id"], "task_id": job["task_id"],
                            "condition": job["condition"], "generator_id": job["generator_id"],
                            "repetition": repetition, "candidate_sha256": sha256(candidate.encode()).hexdigest(),
                            "payload_sha256": payload.semantic_hash})
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("queue.jsonl", queue), ("mapping.jsonl", mapping)):
        rows.sort(key=lambda row: row["evaluation_id"])
        (output / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    report = {"api_calls": 0, "judgments_executed": 0, "simulated_generations": metrics["simulated"],
              "source_log_sha256": source_hash, "configuration_hash": config_hash,
              "configuration_snapshot": config,
              "contract": contract, "configuration": config["judge"]["configuration"],
              "generation_results": metrics["completed"], "generation_statuses": dict(Counter(r["status"] for r in metrics["records"])),
              "prepared_judgments": len(queue), "prompt_version": PROMPT_VERSION,
              "note": "Prepared v2 inputs, not semantic results or main collection. Legacy v1 executors must not execute this queue."}
    (output / "preparation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = prepare(args.source, args.output)
    print(json.dumps({k: report[k] for k in ("prepared_judgments", "judgments_executed", "api_calls")}))
