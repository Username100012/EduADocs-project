"""Consolidate versioned local analyses and prepare blinded judgments offline."""

import argparse
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.judge_prompt import build_llm_judge_prompt
from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.automatic_metrics_v2 import group_presence
from evaluate_pilot import evaluate

LABELS = {"topic": "Tópico", "grade_level": "Nível", "learning_objectives": "Objetivos",
          "duration_minutes": "Duração", "methodology": "Metodologia", "materials": "Materiais",
          "assessment_strategy": "Avaliação"}


def state(requirement, value):
    if value is None:
        return "unavailable"
    result = value["declared_matches_target"] if requirement == "duration_minutes" else value["present"]
    return "matched" if result is True else "not_matched" if result is False else "undetermined"


def consolidate(directory):
    log = directory / "generations.jsonl"
    # Recompute and compare to prevent consolidation of stale/mixed analyses.
    reports = {}
    for version, filename in (("v1", "automatic_metrics.json"), ("v2", "automatic_metrics.v2.json")):
        report = json.loads((directory / filename).read_text(encoding="utf-8"))
        if evaluate(log, version=version) != report:
            raise ValueError("stale or changed metrics: " + filename)
        reports[version] = report
    v1, v2 = reports["v1"], reports["v2"]
    if v2["completed"] != v2["planned"] or v2["simulated"]:
        raise ValueError("consolidation requires a complete real run")
    old = {r["job_id"]: r for r in v1["records"]}
    cells = []
    for row in v2["records"]:
        for requirement in LABELS:
            current = row["metrics"]["requirements"][requirement] if row["metrics"] else None
            previous = old[row["job_id"]]["metrics"]
            previous = previous["requirements"][requirement] if previous else None
            before, after = state(requirement, previous), state(requirement, current)
            cells.append({"job_id": row["job_id"], "task_id": row["task_id"],
                          "generator_id": row["generator_id"], "condition": row["condition"],
                          "repetition": row["repetition"], "requirement": requirement,
                          "target_in_prompt": requirement == "topic" or row["condition"] != "c0",
                          "v1": before, "v2": after, "changed": before != after})
    groups = []
    for task in sorted({c["task_id"] for c in cells}):
        for condition in ("c0", "c1", "c2"):
            for requirement in LABELS:
                selected = [c for c in cells if (c["task_id"], c["condition"], c["requirement"]) == (task, condition, requirement)]
                groups.append({"task_id": task, "condition": condition, "requirement": requirement,
                               "n": len(selected), "v1": dict(Counter(c["v1"] for c in selected)),
                               "v2": dict(Counter(c["v2"] for c in selected))})
    header = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
    operational, stability = [], []
    for condition in ("c0", "c1", "c2"):
        rows = [r for r in v2["records"] if r["condition"] == condition]
        operational.append({"condition": condition, "n": len(rows),
                            "statuses": dict(Counter(r["status"] for r in rows)),
                            "latency_median_seconds": statistics.median(r["operational"]["latency_ms"] / 1000 for r in rows if r["operational"]),
                            "output_tokens": sum(r["operational"]["output_tokens"] or 0 for r in rows if r["operational"]),
                            "cost": None})
        for task in sorted({r["task_id"] for r in rows}):
            subset = [r for r in rows if r["task_id"] == task]
            stability.append({"task_id": task, "condition": condition,
                              "n": len(subset), "distinct_texts": len({r["content_sha256"] for r in subset})})
    paths = ["src/experiment/automatic_metrics.py", "src/experiment/automatic_metrics_v2.py",
             "scripts/evaluate_pilot.py", "scripts/summarize_local_pilot.py",
             "src/experiment/judge_prompt.py", "experiments/llm_judge_response.schema.json"]
    report = {"analysis_type": "exploratory_post_pilot", "source_log_sha256": v2["source_log_sha256"],
              "config_hash": v2["config_hash"], "metrics_version": v2["metrics_version"],
              "code_and_schema_hashes": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
              "changed_cells": sum(c["changed"] for c in cells), "total_cells": len(cells),
              "operational": operational, "stability": stability, "by_task_condition": groups,
              "cells": cells, "semantic_judgments_executed": 0,
              "limitations": ["Post-pilot changes are exploratory, not independent metric validation.",
                              "Lexical evidence is not semantic compliance or educational efficacy.",
                              "C0 did not receive the six requirements beyond topic.",
                              "Fixed-seed repetitions are not independent. No significance tests or composite scores.",
                              "No cloud-versus-local comparison and no factual validation."]}
    source_events = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    texts = {e["job_id"]: e["response"]["content"] for e in source_events[1:]
             if e["event"] == "result" and e["response"]}
    pending = []
    for row in v2["records"]:
        if row["condition"] == "c0" or not row["metrics"]:
            continue
        for requirement, value in row["metrics"]["requirements"].items():
            if state(requirement, value) == "matched":
                continue
            diagnostic = None
            if requirement != "duration_minutes":
                diagnostic = group_presence(
                    [(i, text, None) for i, text in enumerate(texts[row["job_id"]].splitlines(), 1)],
                    [g["aliases"] for g in value["groups"]])
            pending.append({"job_id": row["job_id"], "requirement": requirement,
                            "state": state(requirement, value), "evidence": value,
                            "whole_text_diagnostic_only": diagnostic})
    (directory / "review_cases.v2.json").write_text(json.dumps(
        {"source_log_sha256": v2["source_log_sha256"], "count": len(pending), "cases": pending,
         "note": "C1/C2 unresolved or unmatched lexical checks; not confirmed omissions. Whole-text diagnostic does not replace section-scoped results."},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["remaining_c1_c2_checks_for_review"] = len(pending)
    (directory / "analysis.v2.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (directory / "requirements.v1-v2.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(cells[0]))
        writer.writeheader()
        writer.writerows(cells)
    lines = ["# Análise exploratória do piloto local — v2", "",
             "27 gerações reais, três tarefas, três condições, três repetições. Nenhuma geração adicional. As respostas e a análise v1 permanecem preservadas.", "",
             f"Mudaram os estados de {report['changed_cells']} das {len(cells)} verificações entre v1 e v2. Isso mede efeito da revisão do extrator, não melhora do gerador.", "",
             "## Correspondências por requisito", "",
             "Cada célula é correspondência / não correspondência / indeterminado, sobre nove respostas. Não representa nota de qualidade. Duração compara declaração extraída com o alvo.", "",
             "| Requisito | C0 v1 → v2 | C1 v1 → v2 | C2 v1 → v2 |", "|---|---|---|---|"]
    for requirement, label in LABELS.items():
        entries = []
        for condition in ("c0", "c1", "c2"):
            selected = [c for c in cells if c["condition"] == condition and c["requirement"] == requirement]
            counts = [Counter(c[v] for c in selected) for v in ("v1", "v2")]
            entries.append(" → ".join("/".join(str(count[k]) for k in ("matched", "not_matched", "undetermined")) for count in counts))
        lines.append("| " + " | ".join([label] + entries) + " |")
    lines += ["", "## Por tarefa e condição (v2)", "",
              "| Tarefa | Condição | Requisito | Correspondência | Não correspondência | Indeterminado |", "|---|---|---|---:|---:|---:|"]
    for group in groups:
        n = group["v2"]
        lines.append(f"| {group['task_id']} | {group['condition'].upper()} | {LABELS[group['requirement']]} | {n.get('matched', 0)} | {n.get('not_matched', 0)} | {n.get('undetermined', 0)} |")
    lines += ["", "## Interpretação e pendências", "",
              "A revisão altera extrações sobre os mesmos textos. Não há base para afirmar superioridade pedagógica de C2. Rótulos não reconhecidos, paráfrases, objetivos incompletos e escopo de negação continuam limitando a interpretação. O resultado de C0 contra requisitos que não recebeu não mede obediência.", "",
              "As três repetições não são amostras independentes. Não foram calculadas notas compostas, testes de significância ou custo financeiro presumido. Os dados operacionais e hashes dos textos estão nos JSONs.", "",
              f"Há {len(pending)} verificações C1/C2 sem correspondência ou indeterminadas, listadas com evidências em `review_cases.v2.json`. Isso não representa {len(pending)} omissões confirmadas.", "",
              "O julgamento semântico está preparado offline em `judge_queue.jsonl` (somente prompts e IDs opacos) e `judge_mapping.jsonl` (mapeamento reservado para análise). Nenhuma chamada à julgadora foi realizada. São 81 julgamentos planejados para este lote local; a estimativa de custo e a compatibilidade do acesso devem ser verificadas antes de executar.", "",
              "Gemini permanece pendente. Antes da coleta principal: revisar os casos sem correspondência/indeterminados, congelar as regras e completar a verificação técnica da julgadora. Não alterar respostas ou prompts retrospectivamente para obter melhores métricas.", ""]
    (directory / "ANALYSIS_V2.md").write_text("\n".join(lines), encoding="utf-8")
    prepare_judge_queue(directory, header, log, v2)
    return report


def prepare_judge_queue(directory, header, log_path, metrics):
    tasks = {t["task_id"]: t for t in header["config"]["tasks"]}
    jobs = {j["job_id"]: j for j in header["jobs"]}
    responses = {r["job_id"]: r for r in metrics["records"]}
    queue, mapping = [], []
    repetitions = header["config"]["judge"]["repetitions_per_response"]
    for event in [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()][1:]:
        if event["event"] != "result" or event["status"] != "success":
            continue
        job = jobs[event["job_id"]]
        payload = LessonPlanSemanticPayload.model_validate(tasks[job["task_id"]]["payload"])
        for repetition in range(1, repetitions + 1):
            opaque = sha256((metrics["source_log_sha256"] + event["job_id"] + str(repetition)).encode()).hexdigest()[:32]
            evaluation_id = "eval-" + opaque
            prompt = build_llm_judge_prompt(evaluation_id, payload, event["response"]["content"])
            queue.append({"evaluation_id": evaluation_id, "prompt": prompt.text,
                          "prompt_sha256": prompt.sha256, "prompt_version": prompt.template_version})
            mapping.append({"evaluation_id": evaluation_id, "job_id": job["job_id"],
                            "judge_repetition": repetition, "content_sha256": responses[job["job_id"]]["content_sha256"],
                            "payload_sha256": payload.semantic_hash})
    # Deterministic opaque ordering keeps generator/condition labels out of the queue.
    for filename, rows in (("judge_queue.jsonl", queue), ("judge_mapping.jsonl", mapping)):
        rows.sort(key=lambda row: row["evaluation_id"])
        (directory / filename).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = consolidate(args.directory)
    print(json.dumps({k: report[k] for k in ("changed_cells", "total_cells", "semantic_judgments_executed")}, ensure_ascii=False))
