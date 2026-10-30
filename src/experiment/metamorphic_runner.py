"""Offline simulation runner. Scores here are fixtures, never model evidence."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random
from statistics import median
from uuid import UUID, uuid5

from experiment.judge_metamorphic import load_metamorphic_pairs, metamorphic_suite_hash
from experiment.judge_prompt import (
    JUDGE_CRITERIA, JUDGE_RESPONSE_SCHEMA_VERSION, JUDGE_RUBRIC_VERSION,
    build_llm_judge_prompt,
)
from experiment.judge_response import JudgeResponseValidationError, parse_llm_judge_response


_NAMESPACE = UUID("b607528a-73c5-4b90-8464-633edfe2f2e3")


def run_simulation(suite_path: Path, output_dir: Path, *, seed: int = 42,
                   scenario: str = "expected") -> dict:
    """Run deterministic fixtures through the real prompt builder and parser.

    Scenarios intentionally exercise passing, failing, and incomplete relations.
    Each output directory must be new to prevent mixing or overwriting runs.
    """
    if scenario not in {"expected", "constant", "violations", "incomplete"}:
        raise ValueError("unsupported simulation scenario")
    suite_hash = metamorphic_suite_hash(suite_path)
    seal = suite_path.with_suffix(".sha256").read_text().split()[0]
    if suite_hash != seal:
        raise ValueError("metamorphic suite hash mismatch")
    pairs = load_metamorphic_pairs(suite_path)
    run_id = "simulation-" + uuid5(_NAMESPACE, f"{suite_hash}:{seed}:{scenario}").hex
    jobs = [(pair, member, repetition) for pair in pairs
            for member in ("baseline", "variant") for repetition in (1, 2, 3)]
    random.Random(seed).shuffle(jobs)
    output_dir.mkdir(parents=True, exist_ok=False)
    records = []
    for order, (pair, member, repetition) in enumerate(jobs, 1):
        # Duplicates share the exact prompt; local record IDs distinguish calls.
        identity_member = "duplicate" if pair.kind == "consistency" else member
        evaluation_id = "eval-" + uuid5(
            _NAMESPACE, f"{run_id}:{pair.case_id}:{identity_member}"
        ).hex
        candidate = getattr(pair, member)
        prompt = build_llm_judge_prompt(evaluation_id, pair.payload, candidate)
        for attempt in (1, 2):
            scores = {criterion: 3 for criterion in JUDGE_CRITERIA}
            if member == "variant" and pair.kind in {"omission", "misalignment"}:
                if scenario == "expected":
                    scores[pair.criterion] = 2
            if scenario == "violations" and member == "variant":
                scores = {criterion: 4 for criterion in JUDGE_CRITERIA}
            raw = json.dumps({
                "schema_version": JUDGE_RESPONSE_SCHEMA_VERSION,
                "rubric_version": JUDGE_RUBRIC_VERSION,
                "evaluation_id": evaluation_id,
                "assessments": {criterion: {
                    "score": score, "justification": "Fixture sintética; não é julgamento real."
                } for criterion, score in scores.items()},
            }, ensure_ascii=False)
            if scenario == "incomplete" and pair.case_id == pairs[0].case_id and member == "variant":
                raw = "invalid simulated JSON"
            parsed, error = None, None
            try:
                parsed = parse_llm_judge_response(raw, evaluation_id).model_dump(mode="json")
            except JudgeResponseValidationError as failure:
                error = {"code": failure.code.value, "json_path": failure.json_path}
            record = {
                "record_id": f"{run_id}:{pair.case_id}:{member}:r{repetition}:a{attempt}",
                "simulated": True, "run_id": run_id, "suite_hash": suite_hash,
                "case_id": pair.case_id, "member": member, "repetition": repetition,
                "attempt": attempt, "order": order, "evaluation_id": evaluation_id,
                "prompt": prompt.text, "prompt_hash": prompt.sha256,
                "payload_hash": pair.payload.semantic_hash,
                "candidate_hash": sha256(candidate.encode()).hexdigest(),
                "raw_response": raw, "validated_response": parsed, "error": error,
            }
            records.append(record)
            if error is None:
                break
    report = summarize(pairs, records)
    report.update(simulated=True, run_id=run_id, scenario=scenario, seed=seed,
                  suite_hash=suite_hash, planned_judgments=len(jobs),
                  attempts=len(records), failed_attempts=sum(r["error"] is not None for r in records))
    with (output_dir / "attempts.jsonl").open("x", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    with (output_dir / "report.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def summarize(pairs, records) -> dict:
    details = []
    for pair in pairs:
        members = {}
        stability = {}
        for member in ("baseline", "variant"):
            valid = [r for r in records if r["case_id"] == pair.case_id
                     and r["member"] == member and r["validated_response"] is not None]
            if len(valid) != 3 or len({r["repetition"] for r in valid}) != 3:
                continue
            values = {c: [r["validated_response"]["assessments"][c]["score"]
                          for r in valid] for c in JUDGE_CRITERIA}
            members[member] = {c: median(v) for c, v in values.items()}
            stability[member] = {c: {
                "range": max(v) - min(v),
                "exact_agreement": len(set(v)) == 1,
            } for c, v in values.items()}
        row = {"case_id": pair.case_id, "kind": pair.kind, "medians": members,
               "repetition_stability": stability, "complete": len(members) == 2}
        if row["complete"]:
            criteria = JUDGE_CRITERIA if pair.criterion == "all" else (pair.criterion,)
            deltas = {c: members["variant"][c] - members["baseline"][c] for c in criteria}
            row["deltas"] = deltas
            row["relation_satisfied"] = all(
                d == 0 if pair.operator == "equal" else d <= 0 for d in deltas.values()
            )
            row["directions"] = {c: "decrease" if d < 0 else "increase" if d > 0 else "tie"
                                 for c, d in deltas.items()}
        details.append(row)
    groups = {}
    for kind in sorted({p.kind for p in pairs}):
        rows = [r for r in details if r["kind"] == kind]
        complete = [r for r in rows if r["complete"]]
        groups[kind] = {
            "planned_pairs": len(rows), "complete_pairs": len(complete),
            "incomplete_pairs": len(rows) - len(complete),
            "satisfied_pairs": sum(r["relation_satisfied"] for r in complete),
            "satisfaction_rate": (sum(r["relation_satisfied"] for r in complete) / len(complete)
                                  if complete else None),
            "criterion_direction_counts": dict(Counter(
                direction for r in complete for direction in r["directions"].values()
            )),
        }
    return {"groups": groups, "pairs": details,
            "interpretation": "SIMULAÇÃO: verifica software; não mede confiabilidade de uma LLM."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--scenario", choices=["expected", "constant", "violations", "incomplete"],
                        default="expected")
    args = parser.parse_args()
    suite = Path(__file__).resolve().parents[2] / "experiments/judge_metamorphic_cases.v1.json"
    result = run_simulation(suite, args.output, seed=args.seed, scenario=args.scenario)
    print(json.dumps({k: result[k] for k in ("simulated", "run_id", "planned_judgments", "attempts")}, indent=2))
