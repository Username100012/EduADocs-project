"""Compare two sensitivity configurations on verified identical prompts."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import statistics

from run_judge_sensitivity import TARGETS, summarize

PRICING = {"reference_date": "2026-10-19", "source": "https://developers.openai.com/api/docs/pricing",
           "standard_usd_per_million": {
               "gpt-5.4-mini-2026-03-17": {"input": 0.75, "cached_input": 0.075, "cache_write": None, "output": 4.5},
               "gpt-6.1-sol": {"input": 2.0, "cached_input": 0.1, "cache_write": 2.5, "output": 10.0}}}


def estimate_cost(usage, rates):
    details = usage.get("input_tokens_details") or {}
    cached = details.get("cached_tokens", 0)
    writes = details.get("cache_write_tokens", 0)
    ordinary = usage["input_tokens"] - cached - writes
    if ordinary < 0 or (writes and rates["cache_write"] is None):
        raise ValueError("unsupported or overlapping token accounting")
    return (ordinary * rates["input"] + cached * rates["cached_input"]
            + writes * (rates["cache_write"] or 0) + usage["output_tokens"] * rates["output"]) / 1_000_000


def load(directory, model):
    summary = summarize(directory, model=model, write=False)
    events = [json.loads(line) for line in (directory / "judgments.jsonl").read_text(encoding="utf-8").splitlines()]
    results = [e for e in events[1:] if e["event"] == "result"]
    if summary["completed"] != 36 or summary["statuses"] != {"success": 36} or summary["pending_started"]:
        raise ValueError("comparison requires 36 completed valid judgments per model")
    return summary, events[0], results


def compare(baseline_directory, sol_directory):
    mini, mini_plan, mini_results = load(baseline_directory, "gpt-5.4-mini-2026-03-17")
    sol, sol_plan, sol_results = load(sol_directory, "gpt-6.1-sol")
    old_jobs = {j["evaluation_id"]: j for j in mini_plan["jobs"]}
    if set(old_jobs) != {j["evaluation_id"] for j in sol_plan["jobs"]}:
        raise ValueError("different case identifiers")
    for job in sol_plan["jobs"]:
        old = old_jobs[job["evaluation_id"]]
        for field in ("task_id", "kind", "repetition", "candidate", "candidate_sha256", "payload", "prompt_sha256"):
            if old[field] != job[field]:
                raise ValueError("comparison inputs changed")
        if old["body"]["input"] != job["body"]["input"] or old["body"]["text"] != job["body"]["text"]:
            raise ValueError("prompt or schema changed")
    rows = []
    for original in mini["relations"]:
        other = next(r for r in sol["relations"] if (r["task_id"], r["kind"]) == (original["task_id"], original["kind"]))
        rows.append({"task_id": original["task_id"], "kind": original["kind"], "criterion": original["criterion"],
                     "mini_base": original["baseline"], "mini_variant": original["variant"], "mini_outcome": original["outcome"],
                     "sol_base": other["baseline"], "sol_variant": other["variant"], "sol_outcome": other["outcome"]})
    operational = []
    for summary, plan, results in ((mini, mini_plan, mini_results), (sol, sol_plan, sol_results)):
        model = summary["model"]
        rates = PRICING["standard_usd_per_million"][model]
        operational.append({"model": model, "configuration": plan["configuration"], "usage": summary["usage"],
                            "estimated_usd": sum(estimate_cost(e["raw_response"]["usage"], rates) for e in results),
                            "cached_input_tokens": sum((e["raw_response"]["usage"].get("input_tokens_details") or {}).get("cached_tokens", 0) for e in results),
                            "cache_write_tokens": sum((e["raw_response"]["usage"].get("input_tokens_details") or {}).get("cache_write_tokens", 0) for e in results),
                            "reasoning_tokens": sum((e["raw_response"]["usage"].get("output_tokens_details") or {}).get("reasoning_tokens", 0) for e in results),
                            "median_latency_seconds": statistics.median(e["latency_ms"] / 1000 for e in results),
                            "exact_agreement_triplets": sum(r == 0 for text in summary["medians"] for r in text["score_ranges"].values()),
                            "complete_triplets": 48})
    report = {"same_texts_payloads_prompts_rubric_and_schema_verified": True,
              "configuration_confound": "Sol uses reasoning low, omits temperature/top_p, and caps output at 4096 including reasoning; Mini used none, temperature 0, top_p 1, cap 1200. Not a pure model-only causal comparison.",
              "version_limitation": "Sol's published model identifier has no dated snapshot in the consulted model page. Preserve returned metadata; do not claim immutable version.",
              "pricing": PRICING, "pricing_note": "Estimates at reference-day standard rates, not historical invoices; no taxes, currency conversion or promotional credits. Input accounting treats cache reads/writes as disjoint subsets.",
              "sources": {"mini_log_sha256": mini["source_log_sha256"], "sol_log_sha256": sol["source_log_sha256"]},
              "rows": rows, "operational": operational,
              "outcomes": {"mini": mini["outcomes"], "sol": sol["outcomes"]},
              "limitations": ["Three synthetic pilot-domain tasks and deliberately obvious defects; exploratory, not independent validation.",
                              "Shared controls and repetitions are dependent; no significance tests or overall quality score.",
                              "Choosing a model after these tests requires checking reserved cases before the main study."]}
    (sol_directory / "comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Comparação de sensibilidade — Mini e Sol", "",
             "36 julgamentos válidos por configuração. Verificados textos, payloads, prompts, IDs, rubrica e esquema idênticos. Os resultados do piloto de 81 julgamentos não foram recalculados.", "",
             "## Comparação por defeito", "",
             "| Alteração | Mini: quedas/3 | Sol: quedas/3 | Mini: empates/3 | Sol: empates/3 |", "|---|---:|---:|---:|---:|"]
    for kind in TARGETS:
        selected = [r for r in rows if r["kind"] == kind]
        counts = [sum(r[p + "_outcome"] == direction for r in selected) for direction in ("decrease", "tie") for p in ("mini", "sol")]
        lines.append("| " + " | ".join([kind] + [str(v) for v in counts]) + " |")
    lines += ["", "## Medianas por tarefa", "",
              "| Tarefa | Alteração | Mini: base → variante | Sol: base → variante |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['task_id']} | {row['kind']} | {row['mini_base']} → {row['mini_variant']} | {row['sol_base']} → {row['sol_variant']} |")
    lines += ["", "## Consumo e estabilidade", "",
              "| Modelo | Entrada | Saída | Latência mediana (s) | Estimativa US$ | Trincas com concordância exata |", "|---|---:|---:|---:|---:|---:|"]
    for op in operational:
        lines.append(f"| {op['model']} | {op['usage']['input_tokens']} | {op['usage']['output_tokens']} | {op['median_latency_seconds']:.2f} | {op['estimated_usd']:.4f} | {op['exact_agreement_triplets']}/48 |")
    lines += ["", "Estimativas segundo [preços oficiais](https://developers.openai.com/api/docs/pricing), consultados em 19/10/2026. O JSON registra cache de leitura/escrita e tokens de raciocínio. A chamada técnica Sol fica fora das 36 e desses custos.", "",
              "## Interpretação", "", report["configuration_confound"], "", report["version_limitation"], ""]
    lines += ["- " + note for note in report["limitations"]]
    sol_omission = [r for r in rows if r["kind"] == "omission"]
    if all(r["sol_outcome"] == "decrease" for r in sol_omission):
        lines += ["", "O Sol penalizou a omissão explícita de materiais nas três tarefas, enquanto o Mini empatou com as bases. Isso favorece o Sol neste diagnóstico específico, mas não o valida como juiz geral. Antes de adotá-lo na coleta principal, verificar sensibilidade em casos reservados e registrar definitivamente a configuração. Não substituir retroativamente os julgamentos antigos.", ""]
    else:
        lines += ["", "A omissão não produziu queda estrita em todas as tarefas no Sol. A troca de modelo, sozinha, não demonstrou resolver integralmente a limitação. Examinar as justificativas antes de decidir por alteração da rubrica ou julgadora.", ""]
    (sol_directory / "COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("sol", type=Path)
    args = parser.parse_args()
    report = compare(args.baseline, args.sol)
    print(json.dumps(report["outcomes"]))
