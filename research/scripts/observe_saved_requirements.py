"""Observe labeled fields in existing responses without semantic classification."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.requirement_measurement import observe_requirements, VERSION, LABELS
from evaluate_pilot import evaluate


def observe(directory):
    path = directory / "generations.jsonl"
    metrics = evaluate(path, version="v2")
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    jobs = {j["job_id"]: j for j in events[0]["jobs"]}
    rows = []
    for event in events[1:]:
        if event["event"] != "result":
            continue
        job = jobs[event["job_id"]]
        text = (event["response"] or {}).get("content")
        rows.append({"job_id": job["job_id"], "task_id": job["task_id"], "condition": job["condition"],
                     "generator_id": job["generator_id"], "status": event["status"],
                     "observation": observe_requirements(text, job["payload"]["duration_minutes"]) if text else None})
    groups = []
    for generator, condition in sorted({(j["generator_id"], j["condition"]) for j in jobs.values()}):
        selected = [r for r in rows if r["generator_id"] == generator and r["condition"] == condition]
        available = [r for r in selected if r["observation"]]
        for requirement in LABELS:
            counts = Counter(r["observation"]["fields"][requirement]["observation"] for r in available)
            groups.append({"generator_id": generator, "condition": condition, "requirement": requirement,
                           "analyzable_texts": len(available), "results_without_text": len(selected) - len(available),
                           "counts": {state: counts[state] for state in ("detected", "empty", "not_detected")}})
    report = {"measurement_version": VERSION, "simulated": metrics["simulated"], "api_calls": 0,
              "source_log_sha256": sha256(path.read_bytes()).hexdigest(), "records": rows, "groups": groups,
              "interpretation": "Syntactic field observations only. Not semantic adherence estimates or educational quality. Missing label is not proven omission."}
    (directory / "requirement_observations.v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = observe(args.directory)
    print(json.dumps({"records": len(report["records"]), "groups": len(report["groups"]), "api_calls": 0}))
