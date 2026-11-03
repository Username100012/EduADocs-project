"""Audit saved v1 lexical metrics without changing metrics, prompts or outputs."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.automatic_metrics import evaluate_text, group_presence, normalize

LABELS = {
    "topic": "Tópico", "grade_level": "Nível escolar",
    "learning_objectives": "Objetivos", "duration_minutes": "Duração",
    "methodology": "Metodologia", "materials": "Materiais",
    "assessment_strategy": "Avaliação",
}


def audit_cell(text, task, requirement, baseline):
    lines = [(i, line, None) for i, line in enumerate(text.splitlines(), 1)]
    flags = []
    diagnostic = None
    if requirement == "duration_minutes":
        value = baseline["declared_matches_target"]
        evidence = baseline["declared"]
        for number, line, _ in lines:
            n = normalize(re.sub(r"[*#_]", "", line))
            if re.search(r"\b\d+\s+aulas?\s*\(.*\bcada\b", n):
                flags.append({"type": "multiple_lessons_not_multiplied", "line": number, "text": line})
            if re.search(r"duracao\s+da\s+aula\s*:", n):
                flags.append({"type": "duration_label_not_supported", "line": number, "text": line})
        if baseline["clock_schedule_minutes"] is None:
            flags.append({"type": "schedule_not_extracted_not_proof_of_consistency"})
    else:
        value = baseline["present"]
        evidence = [e for group in baseline["groups"] for e in group["evidence"]]
        diagnostic = group_presence(lines, [g["aliases"] for g in baseline["groups"]])
        if value is not True and diagnostic["present"] is True:
            flags.append({"type": "lexical_evidence_outside_recognized_section"})
        if requirement == "grade_level" and re.search(r"ensino medio", normalize(text)):
            flags.append({"type": "mixed_school_levels_mention_not_target_specificity"})
        if requirement == "topic" and "não funcion" in task["payload"]["topic"]:
            flags.append({"type": "nonfunctional_term_can_trigger_negation_heuristic"})
    return {"baseline_state": "matched" if value is True else "not_matched" if value is False else "undetermined",
            "baseline_evidence": evidence, "diagnostic_whole_text": diagnostic,
            "flags": flags}


def audit(directory):
    log_path = directory / "generations.jsonl"
    metric_path = directory / "automatic_metrics.json"
    raw = log_path.read_bytes()
    stored_raw = metric_path.read_bytes()
    stored = json.loads(stored_raw)
    if stored["source_log_sha256"] != sha256(raw).hexdigest():
        raise ValueError("metrics refer to a different source log")
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    header = events[0]
    jobs = {j["job_id"]: j for j in header["jobs"]}
    tasks = {t["task_id"]: t for t in header["config"]["tasks"]}
    metrics = {r["job_id"]: r for r in stored["records"]}
    results = [e for e in events[1:] if e["event"] == "result"]
    if len(results) != len(metrics) or len({e["job_id"] for e in results}) != len(results):
        raise ValueError("duplicate or missing results")
    cells, text_flags = [], []
    for event in results:
        job = jobs[event["job_id"]]
        if not event["response"]:
            continue
        text = event["response"]["content"]
        recomputed = evaluate_text(text, tasks[job["task_id"]])
        if recomputed != metrics[job["job_id"]]["metrics"]:
            raise ValueError("stored metrics do not reproduce")
        for requirement, baseline in recomputed["requirements"].items():
            cells.append({"job_id": job["job_id"], "task_id": job["task_id"],
                          "condition": job["condition"], "generator_id": job["generator_id"],
                          "requirement": requirement,
                          "target_was_in_prompt": requirement == "topic" or job["condition"] != "c0",
                          **audit_cell(text, tasks[job["task_id"]], requirement, baseline)})
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"[\u4e00-\u9fff]", line):
                text_flags.append({"job_id": job["job_id"], "line": i, "text": line,
                                   "type": "cjk_characters_in_portuguese_output"})
    summaries = []
    for gid, task_id, condition in sorted({(c["generator_id"], c["task_id"], c["condition"]) for c in cells}):
        for requirement in LABELS:
            selected = [c for c in cells if (c["generator_id"], c["task_id"], c["condition"], c["requirement"]) == (gid, task_id, condition, requirement)]
            summaries.append({"generator_id": gid, "task_id": task_id, "condition": condition,
                              "requirement": requirement,
                              "states": dict(Counter(c["baseline_state"] for c in selected)),
                              "whole_text_matches_missed_by_scope": sum(
                                  any(f["type"] == "lexical_evidence_outside_recognized_section" for f in c["flags"]) for c in selected)})
    return {"audit_version": "pilot-metrics-audit-v1", "simulated": header["simulated"],
            "source_log_sha256": sha256(raw).hexdigest(),
            "source_metrics_sha256": sha256(stored_raw).hexdigest(),
            "recomputed_metrics_match": True, "results": len(results),
            "cells": cells, "by_task_condition": summaries, "text_flags": text_flags,
            "interpretation": "Whole-text matching is an extraction diagnostic, not a replacement score or semantic ground truth. No post-hoc rule changes or new generation calls."}


def markdown(report):
    lines = ["# Auditoria das métricas do piloto local", "",
             f"{report['results']} respostas; {len(report['cells'])} células de requisitos. As métricas v1 foram reproduzidas a partir do log original. Respostas, configuração e métricas originais foram preservadas.", "",
             "Correspondência é evidência lexical; não é conformidade semântica. Não correspondência não comprova omissão. Indeterminado significa que o extrator não decidiu.", "",
             "## Por condição (9 respostas em cada condição)", "",
             "| Requisito | Condição | Correspondência | Não correspondência | Indeterminado | Correspondência no texto fora do escopo reconhecido |",
             "|---|---|---:|---:|---:|---:|"]
    for requirement, label in LABELS.items():
        for condition in ("c0", "c1", "c2"):
            cells = [c for c in report["cells"] if c["condition"] == condition and c["requirement"] == requirement]
            counts = Counter(c["baseline_state"] for c in cells)
            missed = sum(any(f["type"] == "lexical_evidence_outside_recognized_section" for f in c["flags"]) for c in cells)
            lines.append(f"| {label} | {condition.upper()} | {counts['matched']} | {counts['not_matched']} | {counts['undetermined']} | {missed} |")
    lines += ["", "## Diagnóstico e consequências", "",
              "- O reconhecimento de seções exige rótulos específicos com dois-pontos e não trata uniformemente títulos numerados e campos em listas. A busca no texto inteiro, com os mesmos aliases, revela evidências perdidas pelo escopo; ela pode incluir exemplos e menções incidentais e não substitui a métrica.",
              "- O nível escolar conta qualquer menção de graduação/ensino superior, inclusive planos que também mencionam ensino médio. Não mede adequação ao nível nem exclusividade do público-alvo.",
              "- Objetivos verificam verbos e conceitos, sem comprovar todos os resultados esperados. Metodologia exige aliases restritos. Materiais e avaliação dependem de seções reconhecidas. Não há validação de qualidade desses requisitos.",
              "- A heurística de negação pode confundir 'não funcionais' com contexto negado. Não se deve resolver isso adicionando aliases apenas para melhorar estes resultados.",
              "- A duração v1 pode interpretar '2 aulas (90 minutos cada)' como 90, sem multiplicar; também ignora 'Duração da aula'. O cronograma em etapas com minutos não é somado. Ausência de contradição detectada não prova consistência.",
              "- C0 recebe apenas tipo de material e tópico. Compará-la aos outros seis requisitos é comparação contra um alvo não informado, e não desobediência a instruções recebidas.",
              "- A dependência da formatação pode distorcer C1 versus C2. Não usar esta tabela para afirmar superioridade de uma condição; não calcular nota composta.", "",
              "## Evidências auditáveis", "",
              "Cada uma das 189 células, seus trechos e linhas, flags e diagnóstico no texto inteiro está em `metrics_audit.json`; o mesmo arquivo contém os 63 agrupamentos por tarefa, condição e requisito. Os hashes vinculam a auditoria aos arquivos de origem.", ""]
    examples = {}
    for cell in report["cells"]:
        for flag in cell["flags"]:
            examples.setdefault(flag["type"], (cell, flag))
    for kind, (cell, flag) in examples.items():
        lines += [f"- `{kind}`: `{cell['job_id']}`, requisito `{cell['requirement']}`" +
                  (f", linha {flag['line']}: {flag['text']}" if "line" in flag else ".")]
    lines += ["", f"Foram sinalizadas {len(report['text_flags'])} ocorrências de caracteres CJK; são alertas técnicos de conteúdo a investigar, não uma classificação validada de idioma.", ""]
    for flag in report["text_flags"]:
        lines.append(f"- `{flag['job_id']}`, linha {flag['line']}: {flag['text']}")
    lines += ["", "## Próximo passo isolado", "",
              "Construir testes de invariância à formatação com exemplos sintéticos e corrigir o extrator em uma nova versão. Congelar as regras antes da coleta principal; recalcular este piloto como análise exploratória, preservando v1. Não regenerar planos nem alegar que ajustes feitos após observar o piloto constituem validação independente.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = audit(args.directory)
    (args.directory / "metrics_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.directory / "METRICS_AUDIT.md").write_text(markdown(report), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("results", "recomputed_metrics_match")}, ensure_ascii=False))
