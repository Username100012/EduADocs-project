"""Report computational proxies and operational coverage; never semantic scores."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import statistics

from evaluate_pilot import evaluate


def distribution(values):
    values = [v for v in values if v is not None]
    quartiles = statistics.quantiles(values, n=4, method="inclusive") if len(values) >= 2 else None
    return {"available": len(values), "median": statistics.median(values) if values else None,
            "minimum": min(values) if values else None, "maximum": max(values) if values else None,
            "iqr": quartiles[2] - quartiles[0] if quartiles else None}


def summarize(directory):
    source = directory / "automatic_metrics.v2.json"
    metrics = json.loads(source.read_text(encoding="utf-8"))
    if evaluate(directory / "generations.jsonl", version="v2") != metrics:
        raise ValueError("stale v2 metrics")
    events = [json.loads(line) for line in (directory / "generations.jsonl").read_text(encoding="utf-8").splitlines()]
    jobs = events[0]["jobs"]
    started = {e["job_id"] for e in events[1:] if e["event"] == "started"}
    records = metrics["records"]
    groups = []
    for task in [None] + sorted({j["task_id"] for j in jobs}):
        for generator, condition in sorted({(j["generator_id"], j["condition"]) for j in jobs}):
            planned = [j for j in jobs if j["generator_id"] == generator and j["condition"] == condition
                       and (task is None or j["task_id"] == task)]
            rows = [r for r in records if r["generator_id"] == generator and r["condition"] == condition
                    and (task is None or r["task_id"] == task)]
            analyzed = [r for r in rows if r["metrics"] and r["metrics"]["requirements"]]
            group = {"task_id": task, "generator_id": generator, "condition": condition,
                     "planned": len(planned), "started": sum(j["job_id"] in started for j in planned),
                     "completed": len(rows), "analyzable_texts": len(analyzed),
                     "statuses": dict(Counter(r["status"] for r in rows)), "requirements": {}, "operational": {}}
            for requirement in ("topic", "grade_level", "learning_objectives", "duration_minutes", "methodology", "materials", "assessment_strategy"):
                values = [r["metrics"]["requirements"][requirement] for r in analyzed]
                states = [v["declared_matches_target"] if requirement == "duration_minutes" else v["present"] for v in values]
                counts = {"matched": sum(v is True for v in states), "not_matched": sum(v is False for v in states),
                          "undetermined": sum(v is None for v in states)}
                group["requirements"][requirement] = {"denominator": len(states), "counts": counts,
                    "proportions": {k: n / len(states) if states else None for k, n in counts.items()},
                    "target_in_prompt": requirement == "topic" or condition != "c0"}
            for key in ("latency_ms", "input_tokens", "output_tokens"):
                group["operational"][key] = distribution([r["operational"].get(key) for r in rows if r["operational"]])
            group["operational"]["word_count"] = distribution([r["metrics"]["word_count"] for r in analyzed])
            groups.append(group)
    report = {"metrics_version": metrics["metrics_version"], "source_log_sha256": metrics["source_log_sha256"],
              "source_metrics_sha256": sha256(source.read_bytes()).hexdigest(), "simulated": metrics["simulated"],
              "analysis_code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "quartile_method": "statistics.quantiles inclusive; IQR null with fewer than two measurements",
              "groups": groups, "composite_score": None,
              "interpretation": "Lexical states use all analyzable texts as denominator, including undetermined. Technical failures remain separately counted; C0 lacks six target requirements. No semantic compliance or pedagogical quality claim."}
    (directory / "primary_metrics.v2.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Indicadores computacionais principais — v2", "",
             "SIMULAÇÃO: respostas fictícias, sem valor experimental." if metrics["simulated"] else "Análise das respostas reais salvas, sem novas chamadas.", "",
             "Resultados de extração textual e operação. Não são notas de qualidade ou taxas comprovadas de atendimento semântico. Os estados são contados sobre todos os textos analisáveis, mantendo indeterminados no denominador.", "",
             "| Gerador | Condição | Planejadas | Iniciadas | Concluídas | Textos analisáveis | Latência mediana ms | IQR ms |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for group in groups:
        if group["task_id"] is None:
            latency = group["operational"]["latency_ms"]
            lines.append(f"| {group['generator_id']} | {group['condition'].upper()} | {group['planned']} | {group['started']} | {group['completed']} | {group['analyzable_texts']} | {latency['median']} | {latency['iqr']} |")
    lines += ["", "| Gerador | Condição | Requisito | Correspondência | Não correspondência | Indeterminado | Denominador |", "|---|---|---|---:|---:|---:|---:|"]
    for group in groups:
        if group["task_id"] is None:
            for requirement, value in group["requirements"].items():
                c = value["counts"]
                lines.append(f"| {group['generator_id']} | {group['condition'].upper()} | {requirement} | {c['matched']} | {c['not_matched']} | {c['undetermined']} | {value['denominator']} |")
    lines += ["", "O JSON também separa tarefas, estados de término, cobertura de tokens e contagem de palavras. IQR usa quartis inclusivos; com menos de duas medidas permanece nulo. Tempos incluem efeitos de rede/carregamento. C0 não recebeu os seis requisitos além do tópico. Não há score composto, falhas com nota zero, testes de significância ou nova chamada à API.", ""]
    (directory / "PRIMARY_METRICS_V2.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = summarize(args.directory)
    print(json.dumps({"groups": len(report["groups"]), "simulated": report["simulated"], "api_calls": 0}))
