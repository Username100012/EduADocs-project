"""Apply existing automatic metrics to saved pilot responses; no API calls."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.automatic_metrics import evaluate_text, operational_metrics, METRICS_VERSION


def evaluate(log_path, *, version="v1"):
    if version not in {"v1", "v2"}:
        raise ValueError("unknown metrics version")
    if version == "v2":
        from experiment.automatic_metrics_v2 import evaluate_text as evaluator, METRICS_VERSION as metrics_version
    else:
        evaluator, metrics_version = evaluate_text, METRICS_VERSION
    raw = log_path.read_bytes()
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    header = events[0]
    if header.get("event") != "plan":
        raise ValueError("missing plan header")
    expected_hash = sha256(json.dumps(header["config"], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    if header["config_hash"] != expected_hash:
        raise ValueError("configuration hash mismatch")
    jobs = {j["job_id"]: j for j in header["jobs"]}
    tasks = {t["task_id"]: t for t in header["config"]["tasks"]}
    rows = []
    started, completed = set(), set()
    for event in events[1:]:
        job_id = event["job_id"]
        if job_id not in jobs:
            raise ValueError("unknown job")
        if event["event"] == "started":
            if job_id in started:
                raise ValueError("duplicate start")
            started.add(job_id)
            continue
        if event["event"] != "result":
            raise ValueError("unknown event")
        if job_id not in started or job_id in completed:
            raise ValueError("duplicate or unstarted result")
        completed.add(job_id)
        job = jobs[event["job_id"]]
        response = event["response"]
        rows.append({"job_id": job["job_id"], "generator_id": job["generator_id"],
                     "task_id": job["task_id"], "condition": job["condition"],
                     "repetition": job["repetition"], "status": event["status"],
                     "error": event["error"],
                     "content_sha256": sha256(response["content"].encode()).hexdigest() if response else None,
                     "metrics": evaluator(response["content"], tasks[job["task_id"]]) if response else None,
                     "operational": operational_metrics(response) if response else None})
    groups = []
    for gid, condition in sorted({(j["generator_id"], j["condition"]) for j in jobs.values()}):
        selected = [r for r in rows if (r["generator_id"], r["condition"]) == (gid, condition)]
        latencies = [r["operational"]["latency_ms"] for r in selected if r["operational"]]
        groups.append({"generator_id": gid, "condition": condition,
                       "completed": len(selected), "statuses": dict(Counter(r["status"] for r in selected)),
                       "median_latency_ms": statistics.median(latencies) if latencies else None,
                       "detected_duration_contradictions": sum(
                           bool(r["metrics"]["requirements"]["duration_minutes"].get(
                               "detected_contradiction", r["metrics"]["requirements"]["duration_minutes"].get("target_mismatch_detected")))
                           for r in selected if r["metrics"] and r["metrics"]["requirements"])})
        if version == "v2":
            groups[-1]["target_duration_mismatches"] = groups[-1].pop("detected_duration_contradictions")
    return {"metrics_version": metrics_version, "simulated": header["simulated"],
            "source_log_sha256": sha256(raw).hexdigest(), "config_hash": header["config_hash"],
            "planned": len(jobs), "completed": len(rows), "groups": groups, "records": rows,
            "limitations": "Lexical proxies only; no pedagogical or factual validation. Fixed-seed repetitions are not independent. Missing extraction does not prove absence. Truncations are preserved."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--version", choices=("v1", "v2"), default="v1")
    args = parser.parse_args()
    report = evaluate(args.directory / "generations.jsonl", version=args.version)
    filename = "automatic_metrics.json" if args.version == "v1" else "automatic_metrics.v2.json"
    (args.directory / filename).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, ensure_ascii=False, indent=2))
