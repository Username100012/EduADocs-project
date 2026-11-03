"""Offline descriptive ceiling audit and traceable justification checks."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.automatic_metrics import normalize
from experiment.automatic_metrics_v2 import duration_metrics
from experiment.judge_prompt import JUDGE_CRITERIA
from experiment.judge_record import JudgeExecutionRecord
from summarize_judgments import LABELS
from run_judgments import load_plan


def arithmetic_alert(justification, text):
    """Only flag explicit addition asserted to exceed a declared duration."""
    normalized = normalize(justification)
    declarations = duration_metrics(text, 0)["declared"]
    targets = {d["minutes"] for d in declarations}
    alerts = []
    for match in re.finditer(r"\b\d+(?:\s*\+\s*\d+)+\b", normalized):
        tail = normalized[match.end():match.end() + 100]
        claim = re.search(r"\b(?:excede|supera|ultrapassa)\b", tail)
        if not claim or re.search(r"\bnao\s+$", tail[:claim.start()]):
            continue
        target = re.search(r"(?:de\s+)?(\d+)\s*minutos", tail)
        if target and float(target[1]) in targets:
            total = sum(int(n) for n in match[0].split("+"))
            if total <= int(target[1]):
                alerts.append({"type": "false_explicit_arithmetic_claim", "expression": match[0],
                               "computed_sum": total, "declared_minutes": int(target[1])})
    return alerts


def audit(directory):
    plan, queue, mapping, jobs, sources = load_plan(directory)
    path = directory / "judgments.jsonl"
    raw = path.read_bytes()
    summary_path = directory / "judgment_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary["source_judgments_sha256"] != sha256(raw).hexdigest():
        raise ValueError("stale judgment summary")
    events = [json.loads(line) for line in raw.decode().splitlines()]
    if events[0] != plan:
        raise ValueError("changed judgment plan")
    rows, alerts = [], []
    for event in events[1:]:
        if event["event"] != "result" or event["status"] != "success":
            continue
        record = JudgeExecutionRecord.model_validate(event["record"])
        link = mapping[event["evaluation_id"]]
        job = jobs[link["job_id"]]
        for criterion, value in record.validated_response.model_dump()["assessments"].items():
            row = {"evaluation_id": event["evaluation_id"], "job_id": job["job_id"],
                   "task_id": job["task_id"], "condition": job["condition"], "criterion": criterion,
                   "judge_repetition": link["judge_repetition"], **value}
            rows.append(row)
            for issue in arithmetic_alert(value["justification"], record.candidate.text):
                alerts.append({**row, **issue})
    if len(rows) != 324 or len({(r["evaluation_id"], r["criterion"]) for r in rows}) != 324:
        raise ValueError("expected 324 unique criterion scores")
    distributions = []
    for condition in ("c0", "c1", "c2"):
        for criterion in JUDGE_CRITERIA:
            selected = [r for r in rows if r["condition"] == condition and r["criterion"] == criterion]
            counts = Counter(r["score"] for r in selected)
            distributions.append({"condition": condition, "criterion": criterion, "n": len(selected),
                                  "counts": {str(i): counts[i] for i in range(1, 5)},
                                  "maximum_score_count": counts[4], "maximum_score_percent": 100 * counts[4] / len(selected)})
    # Compare at task level; repetition indices are not matched C1/C2 samples.
    comparisons = []
    for task in sorted({j["task_id"] for j in jobs.values()}):
        for criterion in JUDGE_CRITERIA:
            groups = {c: [r for r in summary["response_medians"] if r["task_id"] == task
                          and r["criterion"] == criterion and r["condition"] == c] for c in ("c1", "c2")}
            values = {c: statistics.median(r["median"] for r in group) for c, group in groups.items()}
            comparisons.append({"task_id": task, "criterion": criterion, **values,
                                "c2_minus_c1": values["c2"] - values["c1"],
                                "response_medians": {c: [r["median"] for r in group] for c, group in groups.items()}})
    text_groups = defaultdict(list)
    for row in summary["response_medians"]:
        text = sources[row["job_id"]]["response"]["content"]
        text_groups[(sha256(text.encode()).hexdigest(), row["criterion"])].append(row)
    identical_text_variation = []
    for (digest, criterion), group in text_groups.items():
        if len(group) > 1 and len({r["median"] for r in group}) > 1:
            identical_text_variation.append({"content_sha256": digest, "criterion": criterion,
                                             "responses": [{"job_id": r["job_id"], "median": r["median"]} for r in group]})
    # Candidate alerts only: a caveat is not necessarily incompatible with 4.
    caveats = [r for r in rows if r["score"] == 4 and re.search(
        r"\bmas\b|porem|apesar|embora|omiss|lacuna|ruido|incoeren|inconsisten", normalize(r["justification"]))]
    uncertain = [r for r in rows if r["condition"] in ("c1", "c2") and r["score"] < 4]
    report = {"audit_type": "offline_computational_exploratory", "source_judgments_sha256": sha256(raw).hexdigest(),
              "source_summary_sha256": sha256(summary_path.read_bytes()).hexdigest(),
              "distributions": distributions, "task_comparisons": comparisons,
              "arithmetic_errors": alerts, "maximum_score_caveat_candidates": caveats,
              "nonmaximum_c1_c2_justifications": uncertain, "identical_text_median_variation": identical_text_variation,
              "criteria_not_validated": ["No blinded expert review or independent judge added.",
                                         "Automatic caveat detection is a heuristic, not a contradiction label.",
                                         "Arithmetic checking covers only explicit additions and exceeds claims.",
                                         "Task-level differences are descriptive; no significance tests or composite scores."],
              "source_scores_changed": False, "api_calls": 0}
    (directory / "judgment_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Auditoria offline da julgadora", "",
             "324 notas de 81 julgamentos, sobre 27 planos. Nenhuma nova chamada à API; notas, justificativas e arquivos anteriores preservados.", "",
             "## Distribuições e concentração no teto", "",
             "As contagens são de notas individuais, não de amostras independentes. Cada resposta foi julgada três vezes.", "",
             "| Condição | Critério | Nota 1 | Nota 2 | Nota 3 | Nota 4 | % de nota máxima |", "|---|---|---:|---:|---:|---:|---:|"]
    for row in distributions:
        lines.append("| " + " | ".join([row["condition"].upper(), LABELS[row["criterion"]]] +
                     [str(row["counts"][str(i)]) for i in range(1, 5)] + [f"{row['maximum_score_percent']:.1f}%"]) + " |")
    lines += ["", "## C1 versus C2 por tarefa", "",
              "Mediana das três medianas por resposta em cada tarefa. Não há pareamento artificial por índice de repetição.", "",
              "| Tarefa | Critério | C1 | C2 | C2 − C1 |", "|---|---|---:|---:|---:|"]
    for row in comparisons:
        lines.append(f"| {row['task_id']} | {LABELS[row['criterion']]} | {row['c1']} | {row['c2']} | {row['c2_minus_c1']} |")
    lines += ["", "## Justificativas: achados e limites", "",
              f"Foram detectadas {len(alerts)} alegações aritméticas falsas no padrão verificável. O teste não cobre todas as possíveis falhas de justificativa.", ""]
    for alert in alerts:
        job = alert["job_id"]
        text = sources[job]["response"]["content"]
        source_lines = [{"line": i, "text": line} for i, line in enumerate(text.splitlines(), 1)
                        if re.search(r"Introdução|Atividade Principal|Conclusão|Duração", line)]
        lines += [f"- `{alert['evaluation_id']}`, `{job}`, {LABELS[alert['criterion']]}, nota {alert['score']}: {alert['justification']}",
                  f"  Verificação: {alert['expression']} = {alert['computed_sum']}, duração declarada {alert['declared_minutes']}. A afirmação de excesso é falsa; isso não prova que toda a nota deva ser outra."]
        for source in source_lines:
            lines.append(f"  Fonte, linha {source['line']}: {source['text']}")
    lines += ["", f"Há {len(caveats)} justificativas de nota máxima sinalizadas por palavras de ressalva; são candidatas, não contradições confirmadas. Há {len(uncertain)} notas abaixo de 4 em C1/C2, todas preservadas no JSON da auditoria.", "",
              f"Há {len(identical_text_variation)} grupos de texto idêntico/critério com medianas diferentes entre avaliações. Isso expõe variabilidade da julgadora mesmo sem mudança no conteúdo; as respostas repetidas não são independentes.", "",
              "## Decisão metodológica", "",
              "Existe forte concentração em notas máximas em C1/C2. Ela limita a discriminação neste recorte, sem provar que a rubrica seja inválida ou que as condições sejam equivalentes. Não se recomenda ampliar a escala, alterar âncoras ou trocar a julgadora apenas para produzir diferenças entre C1 e C2.", "",
              "O erro aritmético demonstrado impede tratar as justificativas como verdade de referência. A concordância elevada não substitui validação; problemas reais podem ser ignorados ou penalidades podem apoiar-se em afirmações erradas. As notas devem permanecer como estimativa secundária, acompanhadas das métricas computacionais e casos de falha.", "",
              "Próximo passo recomendado: executar testes de sensibilidade com casos sintéticos de defeitos conhecidos (omissão, desalinhamento e contradição temporal), usando os casos metamórficos já definidos. Registrar os resultados separadamente; qualquer revisão posterior deve ser versionada e avaliada em casos não usados no ajuste. Não editar nem substituir as notas deste piloto.", "",
              "A auditoria é computacional e exploratória, sem participantes humanos. Não houve avaliação externa de correção factual ou de eficácia pedagógica. C0 é avaliada contra seis requisitos não informados, de modo que sua diferença não isola estrutura de prompt.", ""]
    (directory / "JUDGMENT_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = audit(args.directory)
    print(json.dumps({"arithmetic_errors": len(report["arithmetic_errors"]),
                      "maximum_score_caveat_candidates": len(report["maximum_score_caveat_candidates"]),
                      "identical_text_median_variation": len(report["identical_text_median_variation"]), "api_calls": 0}))
