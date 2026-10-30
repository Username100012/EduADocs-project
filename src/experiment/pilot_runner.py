"""Sequential, resumable pilot generation; no scoring or judge calls."""

from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import random
from uuid import NAMESPACE_URL, uuid5

from filelock import FileLock

from experiment.prompt_conditions import build_c0_prompt, build_c1_prompt, build_c2_prompt
from experiment.semantic_payload import LessonPlanSemanticPayload
from models import GenerationRequest, LessonPlanParameters
from providers.google_adapter import GoogleAdapter
from providers.ollama_adapter import OllamaAdapter
import requests


def _hash(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def build_plan(config):
    """Validate prompts and parameters for the legacy pilot or main draft."""
    phase = config.get("study_phase", "pilot")
    if phase not in {"pilot", "main"}:
        raise ValueError("unsupported study phase")
    task_count = 12 if phase == "main" else 3
    if config["conditions"] != ["c0", "c1", "c2"] or len(config["tasks"]) != task_count:
        raise ValueError("study requires its configured task count and C0/C1/C2")
    if phase == "main":
        from experiment.task_catalog import ExperimentalTaskCatalog
        ExperimentalTaskCatalog.model_validate({
            "catalog_id": config["catalog_id"], "language": config["language"],
            "tasks": [{"task_id": t["task_id"], "subject_area": t["subject"],
                       "payload": t["payload"]} for t in config["tasks"]]})
    if config["repetitions_per_task_condition"] != 3:
        raise ValueError("pilot requires three repetitions")
    if len({t["task_id"] for t in config["tasks"]}) != task_count:
        raise ValueError("duplicate task IDs")
    if config["execution"]["automatic_retries"] != 0:
        raise ValueError("automatic retries are not implemented")
    generators = config["generators"]
    if set(generators) != {"gemini", "qwen3"}:
        raise ValueError("pilot requires gemini and qwen3")
    jobs = []
    for task in config["tasks"]:
        payload = LessonPlanSemanticPayload.model_validate(task["payload"])
        prompts = {"c0": build_c0_prompt(payload.topic),
                   "c1": build_c1_prompt(payload), "c2": build_c2_prompt(payload)}
        for condition, prompt in prompts.items():
            for repetition in range(1, 4):
                job_id = f"{task['task_id']}:{condition}:r{repetition}"
                jobs.append({"job_id": job_id, "task_id": task["task_id"],
                             "subject": task["subject"], "condition": condition,
                             "repetition": repetition, "payload": payload.model_dump(),
                             "payload_hash": payload.semantic_hash,
                             "prompt": asdict(prompt), "prompt_hash": prompt.sha256})
    jobs = [{**job, "generator_id": gid,
             "job_id": f"{gid}:{job['job_id']}"}
            for gid in generators for job in jobs]
    if len(jobs) != config["planned_generations"] or len(jobs) != task_count * 18:
        raise ValueError("generation count mismatch")
    random.Random(config["execution"]["shuffle_seed"]).shuffle(jobs)
    # Refuse mismatches rather than silently ignoring config edits.
    for job in jobs:
        request = _request(config, job)
        generator = generators[job["generator_id"]]
        parameters = (GoogleAdapter.generation_parameters(request)
                      if generator["provider"] == "google" else
                      OllamaAdapter.generation_parameters(request, generator["generation_config"]))
        if parameters != generator["generation_config"]:
            raise ValueError("adapter parameters differ from pilot configuration")
    return jobs


def _request(config, job):
    p = job["payload"]
    g = config["generators"][job["generator_id"]]
    parameters = g["generation_config"]
    return GenerationRequest(
        execution_id=uuid5(NAMESPACE_URL, _hash(config) + job["job_id"]),
        document_type="lesson_plan", subject=job["subject"], topic=p["topic"],
        grade_level=p["grade_level"], language=config["language"],
        provider=g["provider"], model=g["model"],
        temperature=parameters.get("temperature", 0.7),
        max_tokens=parameters.get("max_output_tokens", parameters.get("num_predict")),
        pedagogical_parameters=LessonPlanParameters(**{
            k: v for k, v in p.items() if k not in {"topic", "grade_level"}
        }),
    )


def _append(stream, record):
    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    stream.flush()
    os.fsync(stream.fileno())


def verify_local_model(generator):
    """Read-only gate: never pulls a model or silently accepts changed weights."""
    host = generator["host"].rstrip("/")
    response = requests.get(host + "/api/tags", timeout=10)
    response.raise_for_status()
    matches = [m for m in response.json()["models"] if m["name"] == generator["model"]]
    if len(matches) != 1 or matches[0]["digest"] != generator["expected_digest"]:
        raise ValueError("Ollama model missing or digest changed")
    response = requests.get(host + "/api/version", timeout=10)
    response.raise_for_status()
    version = response.json()["version"]
    if version != generator["ollama_version"]:
        raise ValueError("Ollama version changed; revise configuration before collection")
    return {"verified_digest": matches[0]["digest"], "verified_version": version}


def run_pilot(config_path: Path, output_dir: Path, *, simulated=True, adapters=None,
              connection_configs=None, max_jobs=None, generator_ids=None):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not simulated and config.get("study_phase") == "main" and config.get("status") != "ready_for_collection":
        raise ValueError("main study is a draft; live collection is not enabled")
    if not simulated and config.get("study_phase") == "main":
        from experiment.main_protocol import verify_frozen
        verify_frozen(config_path)
    jobs = build_plan(config)
    if generator_ids is not None:
        selected = set(generator_ids)
        if not selected or not selected <= set(config["generators"]):
            raise ValueError("unknown or empty generator selection")
        jobs = [job for job in jobs if job["generator_id"] in selected]
    header = {"event": "plan", "simulated": simulated,
              "config": config, "config_hash": _hash(config), "jobs": jobs}
    # JSON round-trip normalizes tuples before comparing persisted data.
    header = json.loads(json.dumps(header))
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "generations.jsonl"
    with FileLock(str(log_path) + ".lock", timeout=0):
        records = []
        if log_path.exists():
            raw = log_path.read_text(encoding="utf-8")
            if not raw.endswith("\n"):
                raise ValueError("incomplete log tail; refusing resume")
            records = [json.loads(line) for line in raw.splitlines()]
            if not records or records[0] != header:
                raise ValueError("configuration, prompts, plan or execution mode changed")
        started, finished = set(), {}
        allowed = {j["job_id"] for j in jobs}
        for record in records[1:]:
            job_id = record["job_id"]
            if job_id not in allowed:
                raise ValueError("unknown job in log")
            if record["event"] == "started" and job_id not in started:
                started.add(job_id)
            elif record["event"] == "result" and job_id in started and job_id not in finished:
                finished[job_id] = record
            else:
                raise ValueError("duplicate or invalid event sequence")
        if started - finished.keys():
            raise ValueError("unresolved started call; refusing automatic duplicate")
        selected_adapters = adapters if adapters is not None else {
            "gemini": GoogleAdapter(), "qwen3": OllamaAdapter()}
        verified = {}
        if not simulated and adapters is None and len(finished) < len(jobs):
            active = {j["generator_id"] for j in jobs}
            if "gemini" in active and not (connection_configs or {}).get("gemini", {}).get("api_key"):
                raise ValueError("Google credential required before mixed collection")
            if "gemini" in active and config.get("study_phase") == "main":
                from importlib.metadata import version
                if version("google-genai") != config["generators"]["gemini"]["sdk_version"]:
                    raise ValueError("Google SDK version changed; revise protocol before collection")
            if "qwen3" in active:
                verified = verify_local_model(config["generators"]["qwen3"])
        count = 0
        from prompting import PromptArtifact
        with log_path.open("a", encoding="utf-8", newline="\n") as stream:
            if not records:
                _append(stream, header)
            for job in jobs:
                if job["job_id"] in finished:
                    continue
                if max_jobs is not None and count >= max_jobs:
                    break
                now = lambda: datetime.now(timezone.utc).isoformat()
                _append(stream, {"event": "started", "job_id": job["job_id"], "at": now()})
                result = {"event": "result", "job_id": job["job_id"],
                          "generator_id": job["generator_id"],
                          "simulated": simulated, "response": None, "error": None}
                try:
                    gid = job["generator_id"]
                    generator = config["generators"][gid]
                    if simulated:
                        from providers.models import ProviderResponse
                        response = ProviderResponse(
                            content="SIMULAÇÃO: resposta de teste, sem valor experimental.",
                            provider=generator["provider"], model=generator["model"],
                            latency_ms=0, finish_reason="STOP" if gid == "gemini" else "stop",
                        )
                    else:
                        connection = dict((connection_configs or {}).get(gid, {}))
                        if generator["provider"] == "ollama":
                            connection.update(
                                host=generator["host"],
                                timeout=generator["timeout_ms"] / 1000,
                                think=generator["think"], keep_alive=generator["keep_alive"],
                                **{k: generator["generation_config"][k] for k in ("seed", "num_ctx")},
                                **verified,
                            )
                        response = selected_adapters[gid].generate(
                            _request(config, job), PromptArtifact(**job["prompt"]),
                            {**connection, "single_attempt": True,
                             "timeout_ms": config["execution"]["timeout_ms"]},
                        )
                    result["response"] = response.model_dump(mode="json")
                    if response.provider.value != generator["provider"] or response.model != generator["model"]:
                        raise ValueError("provider returned a different model or provider")
                    result["status"] = "success" if str(response.finish_reason).lower() == "stop" else "non_stop"
                except Exception as error:
                    code = getattr(error, "code", None)
                    result.update(status="error", error={"type": type(error).__name__,
                                  "code": code if isinstance(code, (str, int)) else None})
                result["at"] = now()
                _append(stream, result)
                finished[job["job_id"]] = result
                count += 1
                if config.get("study_phase") == "main" and result["status"] == "error":
                    break
                if result["error"] and result["error"]["code"] in (401, 402, 403, 404, 429):
                    break
        return {"simulated": simulated, "planned": len(jobs), "completed": len(finished),
                "success": sum(r["status"] == "success" for r in finished.values()),
                "failed_or_non_stop": sum(r["status"] != "success" for r in finished.values())}
