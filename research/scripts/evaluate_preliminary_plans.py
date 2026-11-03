"""Evaluate existing technical preflights without any LLM calls."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.automatic_metrics import evaluate_text, operational_metrics


def main():
    config = json.loads((ROOT / "experiments/pilot_config.json").read_text())
    task = config["tasks"][0]
    records = []
    qwen = ROOT / "artifacts/qwen3-preflight/report.json"
    if qwen.exists():
        raw = json.loads(qwen.read_text(encoding="utf-8-sig"))
        r = raw["raw_response"]
        records.append({"source": str(qwen.relative_to(ROOT)), "model": raw["model"],
                        "finish_reason": r["done_reason"],
                        "metrics": evaluate_text(r["response"], task),
                        "operational": operational_metrics({"latency_ms": raw["wall_ms"],
                            "input_tokens": r.get("prompt_eval_count"),
                            "output_tokens": r.get("eval_count"), "finish_reason": r.get("done_reason")})})
    llama = ROOT / "artifacts/ollama_local_feasibility.json"
    if llama.exists():
        raw = json.loads(llama.read_text(encoding="utf-8-sig"))
        for response, measurement in zip(raw["responses"], raw["measurements"]):
            records.append({"source": str(llama.relative_to(ROOT)), "model": raw["model"],
                            "phase": response["phase"], "finish_reason": measurement["done_reason"],
                            "metrics": evaluate_text(response["text"], task),
                            "operational": operational_metrics({"latency_ms": measurement["wall_ms"],
                                "input_tokens": measurement.get("prompt_eval_count"),
                                "output_tokens": measurement.get("eval_count"),
                                "finish_reason": measurement["done_reason"]})})
    if not records:
        raise SystemExit("No saved preliminary plans found")
    report = {"experimental_data": False, "source_type": "technical_preflights",
              "records": records, "cost": None,
              "note": "No composite scores, no automatic pedagogical judgment; truncated texts remain labelled."}
    path = ROOT / "artifacts/preliminary_automatic_metrics.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for row in records:
        duration = row["metrics"]["requirements"]["duration_minutes"]
        print(row["model"], row.get("phase", ""), "termination:", row["finish_reason"],
              "declared:", [d["minutes"] for d in duration["declared"]],
              "schedule:", duration["clock_schedule_minutes"],
              "contradiction:", duration["detected_contradiction"])


if __name__ == "__main__":
    main()
