"""Build the twelve-task proposal and complete prompt plan without API calls."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from jsonschema import Draft202012Validator
from experiment.task_catalog import ExperimentalTaskCatalog
from experiment.pilot_runner import build_plan, _hash
from experiment.automatic_metrics_v2 import evaluate_text
from experiment.requirement_measurement import observe_requirements


def prepare(config_path, directory):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("study_phase") != "main":
        raise ValueError("main study configuration required")
    catalog_data = {"schema_version": "eduadocs-task-catalog-v1.0.0", "catalog_id": config["catalog_id"],
                    "language": config["language"], "tasks": [{"task_id": t["task_id"],
                       "subject_area": t["subject"], "payload": t["payload"]} for t in config["tasks"]]}
    schema = json.loads((ROOT / "experiments/task_catalog.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(catalog_data)
    catalog = ExperimentalTaskCatalog.model_validate(catalog_data)
    pilot = json.loads((ROOT / "experiments/pilot_config.json").read_text(encoding="utf-8"))
    pilot_topics = {t["payload"]["topic"] for t in pilot["tasks"]}
    if any(t["payload"]["topic"] in pilot_topics for t in config["tasks"]):
        raise ValueError("main catalog reuses an exact pilot topic")
    for task in config["tasks"]:
        anchors = task["textual_evidence"]
        for key in ("topic_concept_groups", "required_resource_groups", "assessment_action_groups"):
            if not anchors[key] or any(not group or any(not alias.strip() for alias in group) for group in anchors[key]):
                raise ValueError("empty lexical groups")
    jobs = build_plan(config)
    reference_checks = []
    for task in config["tasks"]:
        payload = task["payload"]
        labels = (("Tópico", "topic"), ("Nível", "grade_level"), ("Objetivos", "learning_objectives"),
                  ("Duração", "duration_minutes"), ("Metodologia", "methodology"),
                  ("Materiais", "materials"), ("Avaliação", "assessment_strategy"))
        text = "\n".join(f"{label}: {payload[key]}" + (" minutos" if key == "duration_minutes" else "")
                         for label, key in labels)
        metrics = evaluate_text(text, task)
        observations = observe_requirements(text, payload["duration_minutes"])
        states = {k: v["declared_matches_target"] if k == "duration_minutes" else v["present"]
                  for k, v in metrics["requirements"].items()}
        reference_checks.append({"task_id": task["task_id"], "reference_text": text, "states": states,
                                 "nonpositive_fields": [k for k, value in states.items() if value is not True],
                                 "metrics": metrics, "observations": observations})
    contract = config["judge"].get("contract")
    if contract:
        for name, expected in contract["artifact_sha256"].items():
            if sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError("closed judge contract artifact changed: " + name)
    report = {"status": config["status"], "api_calls": 0, "live_enabled": False,
              "config_hash": _hash(config), "catalog_hash": catalog.catalog_hash,
              "tasks": len(catalog.tasks), "by_subject": dict(Counter(t.subject_area for t in catalog.tasks)),
              "prompt_conditions": len(catalog.tasks) * 3, "planned_generations": len(jobs),
              "planned_judgments_if_all_valid": len(jobs) * config["judge"]["repetitions_per_response"],
              "same_payload_c1_c2_validated": True, "json_schema_valid": True,
              "literal_payload_checks": reference_checks,
              "literal_payloads_with_nonpositive_fields": sum(bool(r["nonpositive_fields"]) for r in reference_checks),
              "observable_fields_detected": sum(v["observation"] == "detected" for row in reference_checks
                                                for v in row["observations"]["fields"].values()),
              "observable_fields_planned": len(reference_checks) * 7,
              "judge_contract": contract,
              "readiness_requirements": config["readiness_requirements"],
              "code_and_schema_hashes": {name: sha256((ROOT / name).read_bytes()).hexdigest() for name in (
                  "src/experiment/prompt_conditions.py", "src/experiment/pilot_runner.py",
                  "src/experiment/automatic_metrics_v2.py", "experiments/task_catalog.schema.json",
                  "src/experiment/judge_prompt.py", "experiments/llm_judge_response.schema.json",
                  "src/experiment/judge_contract_v2.py", "experiments/judge_response.v2.schema.json",
                  "src/experiment/requirement_measurement.py")}}
    if len(jobs) != 216 or report["planned_judgments_if_all_valid"] != 648:
        raise ValueError("main counts mismatch")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "preparation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (directory / "generation_plan.json").write_text(json.dumps({"config": config, "config_hash": _hash(config),
                                                               "jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Preparação offline do estudo principal", "",
             ("Plano do protocolo congelado; esta preparação não inicia a coleta nem valida os construtos." if config.get("freeze") else "Preparação local anterior ao selo final; não inicia a coleta."), "",
             "12 tarefas autorais; quatro por disciplina; 36 prompts distintos (12 tarefas × três condições); 216 gerações previstas com dois geradores e três repetições; até 648 julgamentos se todas as gerações forem válidas.", "",
             "O catálogo passou no esquema JSON e no modelo local; C1/C2 derivam da mesma instância de payload. Isso valida o contrato de software, não a qualidade das tarefas ou das métricas.", "",
             "| Tarefa | Disciplina | Tópico | Referência SBC |", "|---|---|---|---|"]
    for task in config["tasks"]:
        mapping = task["curricular_mapping"]
        lines.append(f"| {task['task_id']} | {task['subject']} | {task['payload']['topic']} | {mapping['competency_id']}, p. {mapping['printed_page']} |")
    lines += ["", "Os tópicos, objetivos, duração, metodologia e aliases são escolhas autorais. O vínculo SBC é um recorte amplo e não equivale a validação, currículo obrigatório ou dificuldade equivalente.", "",
              "## Mensuração e diagnóstico legado", "",
              f"O observador de campos detectou {report['observable_fields_detected']}/{report['observable_fields_planned']} campos nas renderizações literais. Isso verifica detecção sintática nos formatos testados, não cumprimento semântico, qualidade das tarefas ou validade pedagógica.", "",
              f"No diagnóstico lexical legado v2, {report['literal_payloads_with_nonpositive_fields']}/12 tarefas têm ao menos um estado não correspondente/indeterminado. Esses textos não são planos gerados. O diagnóstico foi preservado sem ajustar tarefas ou aliases; não é a definição de atendimento semântico.", ""]
    for check in reference_checks:
        if check["nonpositive_fields"]:
            lines.append(f"- {check['task_id']}: {', '.join(check['nonpositive_fields'])}.")
    lines += ["", "As observações sintáticas não usam aliases, heurísticas de negação ou conceitos do tópico para classificar atendimento. O contrato v2 reserva a estimativa semântica por requisito à julgadora, com evidências verificáveis; validar evidências não prova o acerto da estimativa.", "",
              "## Condições de execução", ""]
    lines += ["- " + requirement for requirement in report["readiness_requirements"]]
    if not report["readiness_requirements"]:
        lines += ["- Verificar o selo e os hashes antes de chamadas reais; o runtime Ollama precisa corresponder ao digest/versão fixados."]
    lines += ["", "O executor compartilhado aceita o plano de 12 tarefas e simulação, mas bloqueia coleta principal real enquanto a configuração estiver em rascunho. O plano prevê uso do Sol; a configuração ativa e os julgamentos anteriores não foram substituídos.", ""]
    (directory / "PREPARATION.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "experiments/main_config.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/main-preparation")
    args = parser.parse_args()
    report = prepare(args.config, args.output)
    print(json.dumps({k: report[k] for k in ("tasks", "planned_generations", "planned_judgments_if_all_valid", "api_calls", "status")}))
