"""Describe ordinal judge scores; preserve within-response repetition hierarchy."""

import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.judge_prompt import JUDGE_CRITERIA
from experiment.judge_record import JudgeExecutionRecord
from experiment.judge_response import parse_llm_judge_response
from run_judgments import load_plan

LABELS = {"semantic_fidelity": "Fidelidade à tarefa", "instructional_alignment": "Alinhamento interno",
          "grade_appropriateness": "Adequação ao nível", "coherence_feasibility": "Coerência e exequibilidade"}


def summarize(directory):
    plan, queue, mapping, jobs, sources = load_plan(directory)
    path = directory / "judgments.jsonl"
    raw = path.read_bytes()
    if not raw.endswith(b"\n"):
        raise ValueError("incomplete log tail")
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    if events[0] != plan:
        raise ValueError("changed judgment plan")
    started, results = set(), {}
    for event in events[1:]:
        eid = event["evaluation_id"]
        if eid not in mapping:
            raise ValueError("unknown evaluation")
        if event["event"] == "started" and eid not in started:
            started.add(eid)
        elif event["event"] == "result" and eid in started and eid not in results:
            results[eid] = event
        else:
            raise ValueError("duplicate or invalid judgment event")
    scores, grouped = [], defaultdict(list)
    for eid, event in results.items():
        if event["status"] != "success":
            continue
        record = JudgeExecutionRecord.model_validate(event["record"])
        parsed = parse_llm_judge_response(event["raw_text"], eid)
        link = mapping[eid]
        job = jobs[link["job_id"]]
        request = next(r for r in plan["requests"] if r["evaluation_id"] == eid)
        if (record.validated_response != parsed or record.evaluation_id != eid
                or record.raw_response != event["raw_text"] or record.prompt.text != request["body"]["input"]
                or record.candidate.sha256 != link["content_sha256"]
                or record.repetition != link["judge_repetition"]
                or record.judge_configuration.model_dump(mode="json") != plan["configuration"]):
            raise ValueError("judgment record evidence mismatch")
        assessments = parsed.model_dump()["assessments"]
        for criterion in JUDGE_CRITERIA:
            assessment = assessments[criterion]
            row = {"evaluation_id": eid, "job_id": job["job_id"], "task_id": job["task_id"],
                   "generator_id": job["generator_id"], "condition": job["condition"],
                   "generation_repetition": job["repetition"], "judge_repetition": link["judge_repetition"],
                   "criterion": criterion, "score": assessment["score"], "justification": assessment["justification"]}
            scores.append(row)
            grouped[(job["job_id"], criterion)].append(row)
    medians = []
    for (job_id, criterion), rows in sorted(grouped.items()):
        job = jobs[job_id]
        values = [r["score"] for r in rows]
        complete = len(values) == 3
        medians.append({"job_id": job_id, "task_id": job["task_id"], "generator_id": job["generator_id"],
                        "condition": job["condition"], "criterion": criterion, "valid_judgments": len(values),
                        "complete_triplet": complete, "median": statistics.median(values) if complete else None,
                        "minimum": min(values), "maximum": max(values), "range": max(values) - min(values),
                        "exact_agreement": len(set(values)) == 1 if complete else None})
    summaries = []
    for task in [None] + sorted({j["task_id"] for j in jobs.values()}):
        for condition in ("c0", "c1", "c2"):
            for criterion in JUDGE_CRITERIA:
                selected = [r for r in medians if r["condition"] == condition and r["criterion"] == criterion
                            and r["complete_triplet"] and (task is None or r["task_id"] == task)]
                values = [r["median"] for r in selected]
                summaries.append({"task_id": task, "condition": condition, "criterion": criterion,
                                  "complete_responses": len(values), "median": statistics.median(values) if values else None,
                                  "minimum": min(values) if values else None, "maximum": max(values) if values else None,
                                  "response_median_distribution": dict(Counter(values)),
                                  "exact_agreement_triplets": sum(r["exact_agreement"] for r in selected),
                                  "maximum_within_response_range": max((r["range"] for r in selected), default=None)})
    usages = [(e.get("raw_response") or {}).get("usage") or {} for e in results.values()]
    report = {"model": plan["configuration"]["model"], "planned_judgments": 81,
              "completed_judgments": len(results), "successful_judgments": sum(e["status"] == "success" for e in results.values()),
              "pending_started": sorted(started - results.keys()), "statuses": dict(Counter(e["status"] for e in results.values())),
              "source_judgments_sha256": sha256(raw).hexdigest(), "source_hashes": plan["source_hashes"],
              "configuration": plan["configuration"], "summaries": summaries, "response_medians": medians,
              "agreement": {"complete_triplets": sum(r["complete_triplet"] for r in medians),
                            "exact_agreement_triplets": sum(r["exact_agreement"] is True for r in medians),
                            "maximum_score_range": max((r["range"] for r in medians), default=None)},
              "analysis_code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "usage": {key: sum(u.get(key, 0) for u in usages) for key in ("input_tokens", "output_tokens", "total_tokens")},
              "cached_input_tokens": sum((u.get("input_tokens_details") or {}).get("cached_tokens", 0) for u in usages),
              "total_latency_seconds": sum(e["latency_ms"] for e in results.values()) / 1000,
              "financial_cost": None, "financial_cost_note": "No unverified price assumption; consult billing for actual charge.",
              "analysis_type": "exploratory_secondary_llm_estimate",
              "limitations": ["Judge scores are automated estimates, not human or pedagogical validation.",
                              "No factual correctness or learning efficacy claims.",
                              "C0 did not receive the six requirements beyond topic.",
                              "Fixed-seed generation repetitions and judge repetitions are not independent samples.",
                              "Only complete three-judgment sets enter response medians; failures are not scored zero.",
                              "No composite score, significance tests or cloud-generator comparison."]}
    (directory / "judgment_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, rows in (("judgment_scores.csv", scores), ("judgment_response_medians.csv", medians), ("judgment_groups.csv", summaries)):
        if rows:
            with (directory / name).open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    lines = ["# Julgamentos semânticos do piloto local", "",
             f"Modelo: `{report['model']}`. Concluídos {len(results)}/81 julgamentos; {report['successful_judgments']} válidos. O teste técnico prévio não entra neste lote.", "",
             "Escala ordinal de 1 a 4. Primeiro é calculada a mediana de três julgamentos de cada resposta; depois, a mediana dessas medianas por condição. Intervalos abaixo são mínimo–máximo entre medianas das respostas, não intervalos de confiança.", "",
             "| Critério | C0 | C1 | C2 |", "|---|---|---|---|"]
    for criterion in JUDGE_CRITERIA:
        entries = []
        for condition in ("c0", "c1", "c2"):
            row = next(r for r in summaries if r["task_id"] is None and r["condition"] == condition and r["criterion"] == criterion)
            entries.append(f"{row['median']} [{row['minimum']}–{row['maximum']}], n={row['complete_responses']}")
        lines.append("| " + " | ".join([LABELS[criterion]] + entries) + " |")
    lines += ["", "## Por tarefa e condição", "",
              "| Tarefa | Condição | Critério | Mediana | Mín.–máx. | Trincas em concordância exata |", "|---|---|---|---:|---|---|"]
    for row in summaries:
        if row["task_id"]:
            lines.append(f"| {row['task_id']} | {row['condition'].upper()} | {LABELS[row['criterion']]} | {row['median']} | {row['minimum']}–{row['maximum']} | {row['exact_agreement_triplets']}/{row['complete_responses']} |")
    lines += ["", "## Uso e limites", "",
              f"Concordância exata: {report['agreement']['exact_agreement_triplets']}/{report['agreement']['complete_triplets']} trincas por resposta/critério. Amplitude máxima dentro de uma trinca: {report['agreement']['maximum_score_range']} ponto(s). Concordância não comprova validade das notas.", "",
              f"Tokens de entrada: {report['usage']['input_tokens']}; saída: {report['usage']['output_tokens']}; entrada em cache: {report['cached_input_tokens']}. Soma das latências: {report['total_latency_seconds']:.2f} s. O custo monetário não foi presumido.", ""]
    lines += ["- " + note for note in report["limitations"]]
    lines += ["", "As justificativas e as 324 notas individuais previstas ficam em `judgment_scores.csv`; as medianas por plano em `judgment_response_medians.csv`; respostas brutas, prompts, configuração e erros em `judgments.jsonl`. O resumo deve ser lido junto da análise lexical v2. Diferenças descritivas não estabelecem superioridade geral de uma condição.", ""]
    (directory / "JUDGMENT_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = summarize(args.directory)
    print(json.dumps({k: report[k] for k in ("completed_judgments", "successful_judgments", "statuses", "usage")}, ensure_ascii=False))
