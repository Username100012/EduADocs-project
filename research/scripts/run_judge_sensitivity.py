"""Controlled synthetic judge sensitivity checks, separate from the pilot."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import random
import statistics
import sys
from time import perf_counter

from filelock import FileLock
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_openai_judge import read_key, redact, request_body
from experiment.judge_prompt import build_llm_judge_prompt, JUDGE_CRITERIA
from experiment.judge_response import parse_llm_judge_response, JudgeResponseValidationError
from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.pilot_runner import _append, _hash

TARGETS = {"omission": "semantic_fidelity", "misalignment": "instructional_alignment",
           "time_contradiction": "coherence_feasibility"}


def build_plan(model=None):
    config = json.loads((ROOT / "experiments/pilot_config.json").read_text(encoding="utf-8"))
    judge = json.loads((ROOT / "experiments/judge_model_selection.v1.json").read_text(encoding="utf-8"))["judge_configuration"]
    if model is not None and model != judge["model"]:
        if model != "gpt-6.1-sol":
            raise ValueError("unsupported comparison model")
        judge.update(model=model, model_version=model, temperature=None, max_output_tokens=4096)
        judge["provider_parameters"].update(reasoning_effort="low", top_p=None)
    schema = json.loads((ROOT / "experiments/llm_judge_response.schema.json").read_text(encoding="utf-8"))
    jobs = []
    for task in config["tasks"]:
        p = task["payload"]
        payload = LessonPlanSemanticPayload.model_validate(p)
        sections = [f"Tópico: {p['topic']}", f"Nível: {p['grade_level']}",
                    f"Objetivos: {p['learning_objectives']}", f"Duração total: {p['duration_minutes']} minutos",
                    f"Metodologia: {p['methodology']}", f"Materiais: {p['materials']}",
                    "Introdução (5 minutos): apresentar o problema e mobilizar os conhecimentos prévios.",
                    "Desenvolvimento (15 minutos): discutir os conceitos e demonstrar como resolver o problema.",
                    f"Prática colaborativa (20 minutos): em grupos, {p['learning_objectives']}. O professor acompanha as soluções e fornece retorno.",
                    f"Avaliação (10 minutos): {p['assessment_strategy']}"]
        baseline = "\n".join(sections)
        omission = "\n".join(line for i, line in enumerate(sections) if i != 5)
        misalignment = "\n".join(sections[:-1] + ["Avaliação (10 minutos): listar capitais brasileiras; a nota depende exclusivamente da grafia dos nomes das capitais."])
        timing = baseline.replace("Prática colaborativa (20 minutos)", "Prática colaborativa (70 minutos)")
        variants = {"baseline": baseline, "omission": omission, "misalignment": misalignment,
                    "time_contradiction": timing}
        if p["duration_minutes"] != 50 or timing == baseline:
            raise ValueError("synthetic time control requires the frozen 50-minute tasks")
        for kind, text in variants.items():
            for repetition in (1, 2, 3):
                eid = "eval-" + _hash({"suite": "judge-sensitivity-v1", "task": task["task_id"],
                                      "payload": p, "candidate": text, "repetition": repetition})[:32]
                prompt = build_llm_judge_prompt(eid, payload, text)
                jobs.append({"evaluation_id": eid, "task_id": task["task_id"], "kind": kind,
                             "repetition": repetition, "payload": p, "candidate": text,
                             "candidate_sha256": sha256(text.encode()).hexdigest(), "prompt_sha256": prompt.sha256,
                             "body": request_body(judge, prompt.text, schema)})
    random.Random(42).shuffle(jobs)
    return {"event": "plan", "suite": "judge-sensitivity-v1", "synthetic": True,
            "configuration": judge, "schema": schema, "jobs": jobs, "automatic_retries": 0,
            "expected_relations": {k: {"criterion": c, "strict_decrease_expected": True} for k, c in TARGETS.items()},
            "baseline_stage_minutes": [5, 15, 20, 10], "time_variant_stage_minutes": [5, 15, 70, 10],
            "declared_minutes": 50, "source_config_sha256": sha256((ROOT / "experiments/pilot_config.json").read_bytes()).hexdigest()}


def read_events(path, plan):
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8")
    if not raw.endswith("\n"):
        raise ValueError("incomplete log")
    events = [json.loads(line) for line in raw.splitlines()]
    if not events or events[0] != plan:
        raise ValueError("sensitivity plan changed")
    return events


def completed_events(events, plan):
    allowed = {j["evaluation_id"] for j in plan["jobs"]}
    started, finished = set(), {}
    for event in events[1:]:
        eid = event["evaluation_id"]
        if eid not in allowed:
            raise ValueError("unknown sensitivity job")
        if event["event"] == "started" and eid not in started:
            started.add(eid)
        elif event["event"] == "result" and eid in started and eid not in finished:
            finished[eid] = event
        else:
            raise ValueError("duplicate or invalid sensitivity event")
    return started, finished


def execute(directory, key, *, post=None, max_jobs=None, model=None):
    post = post or requests.post
    plan = build_plan(model)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "judgments.jsonl"
    with FileLock(str(path) + ".lock", timeout=0):
        events = read_events(path, plan)
        started, finished = completed_events(events, plan)
        if started - finished.keys():
            raise ValueError("unresolved started call; no automatic duplicate")
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            if not events:
                _append(stream, plan)
            count = 0
            for job in plan["jobs"]:
                eid = job["evaluation_id"]
                if eid in finished:
                    continue
                if max_jobs is not None and count >= max_jobs:
                    break
                now = lambda: datetime.now(timezone.utc).isoformat()
                _append(stream, {"event": "started", "evaluation_id": eid, "at": now()})
                start = perf_counter()
                event = {"event": "result", "evaluation_id": eid, "status": "transport_error",
                         "http_status": None, "raw_response": None, "validated_response": None, "error": None}
                try:
                    response = post("https://api.openai.com/v1/responses", headers={"Authorization": "Bearer " + key},
                                    json=job["body"], timeout=90)
                    raw = redact(response.json(), key)
                    event.update(http_status=response.status_code, raw_response=raw,
                                 request_id=response.headers.get("x-request-id"))
                    if not response.ok:
                        event.update(status="api_error", error=raw.get("error"))
                    elif raw.get("model") != plan["configuration"]["model"]:
                        event["status"] = "model_mismatch"
                    elif raw.get("status") != "completed":
                        event["status"] = "incomplete_response"
                    else:
                        text = "".join(c["text"] for item in raw.get("output", []) for c in item.get("content", []) if c.get("type") == "output_text")
                        event["raw_text"] = text
                        try:
                            parsed = parse_llm_judge_response(text, eid)
                            event.update(status="success", validated_response=parsed.model_dump(mode="json"))
                        except JudgeResponseValidationError as error:
                            event.update(status="validation_error", error={"code": error.code.value})
                except (requests.RequestException, ValueError) as error:
                    event["error"] = {"type": type(error).__name__}
                event.update(at=now(), latency_ms=(perf_counter() - start) * 1000)
                _append(stream, redact(event, key))
                finished[eid] = event
                count += 1
                print(json.dumps({"completed": len(finished), "planned": 36, "status": event["status"]}), flush=True)
                if event["http_status"] in (401, 403, 404, 429):
                    break
    return {"completed": len(finished), "planned": 36}


def summarize(directory, *, model=None, write=True):
    plan = build_plan(model)
    path = directory / "judgments.jsonl"
    events = read_events(path, plan)
    started, finished = completed_events(events, plan)
    medians = []
    for task in sorted({j["task_id"] for j in plan["jobs"]}):
        for kind in ("baseline", *TARGETS):
            jobs = [j for j in plan["jobs"] if j["task_id"] == task and j["kind"] == kind]
            valid = []
            for job in jobs:
                event = finished.get(job["evaluation_id"])
                if event and event["status"] == "success":
                    parsed = parse_llm_judge_response(event["raw_text"], job["evaluation_id"]).model_dump(mode="json")
                    if parsed != event["validated_response"]:
                        raise ValueError("saved validation differs")
                    valid.append(parsed)
            scores = {c: [r["assessments"][c]["score"] for r in valid] for c in JUDGE_CRITERIA}
            medians.append({"task_id": task, "kind": kind, "valid_judgments": len(valid),
                            "medians": {c: statistics.median(v) if len(v) == 3 else None for c, v in scores.items()},
                            "score_ranges": {c: max(v) - min(v) if len(v) == 3 else None for c, v in scores.items()}})
    relations = []
    for row in medians:
        if row["kind"] == "baseline":
            continue
        baseline = next(r for r in medians if r["task_id"] == row["task_id"] and r["kind"] == "baseline")
        criterion = TARGETS[row["kind"]]
        before, after = baseline["medians"][criterion], row["medians"][criterion]
        delta = after - before if before is not None and after is not None else None
        relations.append({"task_id": row["task_id"], "kind": row["kind"], "criterion": criterion,
                          "baseline": before, "variant": after, "delta": delta,
                          "outcome": "incomplete" if delta is None else "decrease" if delta < 0 else "increase" if delta > 0 else "tie",
                          "strict_decrease_detected": delta < 0 if delta is not None else None})
    usages = [(e.get("raw_response") or {}).get("usage") or {} for e in finished.values()]
    omission_justifications = []
    for job in plan["jobs"]:
        event = finished.get(job["evaluation_id"])
        if job["kind"] == "omission" and event and event["status"] == "success":
            omission_justifications.append({"task_id": job["task_id"], "evaluation_id": job["evaluation_id"],
                "repetition": job["repetition"], "removed_materials": job["payload"]["materials"],
                **event["validated_response"]["assessments"]["semantic_fidelity"]})
    report = {"suite": plan["suite"], "synthetic": True, "simulated": False,
              "model": plan["configuration"]["model"], "planned": 36, "completed": len(finished),
              "statuses": dict(Counter(e["status"] for e in finished.values())), "pending_started": sorted(started - finished.keys()),
              "source_log_sha256": sha256(path.read_bytes()).hexdigest(), "medians": medians,
              "relations": relations, "outcomes": dict(Counter(r["outcome"] for r in relations)),
              "omission_justifications": omission_justifications,
              "usage": {k: sum(u.get(k, 0) for u in usages) for k in ("input_tokens", "output_tokens", "total_tokens")},
              "limitations": ["Constructed perturbations are diagnostic expectations, not validated gold-standard scores.",
                              "Three synthetic tasks reuse pilot target payloads; no independent generalization validation.",
                              "Shared baseline for three variants; comparisons and repeated judgments are dependent.",
                              "A tie is not strict defect sensitivity. Baseline is not assumed to deserve score 4.",
                              "No factual, human or pedagogical efficacy validation; no significance tests or rubric changes.",
                              "A generic resource reference can remain implicit after removal of the explicit materials field.",
                              "No claim of complete defect isolation across semantic criteria; inspect all four scores."]}
    if write:
        (directory / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Sensibilidade da julgadora — casos sintéticos", "",
             f"{len(finished)}/36 julgamentos realizados; modelo `{report['model']}`. Resultados separados do piloto de 81 julgamentos.", "",
             "Três tarefas de Computação, quatro textos por tarefa e três julgamentos por texto. As versões-base são sintéticas e não foram presumidas perfeitas. A única linha retirada na omissão é o campo de materiais; a avaliação é substituída por capitais brasileiras no desalinhamento; na contradição temporal a prática passa de 20 para 70 minutos, elevando a soma de 50 para 100 enquanto a duração declarada permanece 50.", "",
             "Relações e critério-alvo definidos antes das chamadas. Queda estrita é distinguida de empate e aumento; não se calcula uma nota geral nem se atribui zero a falhas.", "",
             "| Tarefa | Alteração | Critério-alvo | Base | Variante | Diferença | Resultado |", "|---|---|---|---:|---:|---:|---|"]
    for r in relations:
        lines.append(f"| {r['task_id']} | {r['kind']} | {r['criterion']} | {r['baseline']} | {r['variant']} | {r['delta']} | {r['outcome']} |")
    lines += ["", "Contagens: " + json.dumps(report["outcomes"], ensure_ascii=False) + ". Cada comparação usa a mediana dos três julgamentos, e as três alterações compartilham a mesma base em cada tarefa.", "",
              "As notas dos quatro critérios para cada texto estão em `report.json`; prompts, candidatos, configuração, respostas brutas, justificativas e erros em `judgments.jsonl`.", ""]
    lines += ["## Justificativas nos casos de omissão", ""]
    for row in omission_justifications:
        lines.append(f"- `{row['evaluation_id']}`, {row['task_id']}, nota {row['score']}: {row['justification']}")
    lines += ["", "## Limites", ""]
    lines += ["- " + limit for limit in report["limitations"]]
    lines += ["", "Interpretação: quedas demonstram resposta às alterações neste conjunto limitado; não estabelecem confiabilidade geral. Empates ou aumentos exigem examinar o contexto e as justificativas antes de revisar a rubrica. O piloto original permanece preservado.", ""]
    if len(finished) == 36 and all(e["status"] == "success" for e in finished.values()):
        lines += ["## Resultado observado e decisão", ""]
        for kind, criterion in TARGETS.items():
            subset = [r for r in relations if r["kind"] == kind]
            lines.append(f"- {kind} ({criterion}): {sum(r['outcome'] == 'decrease' for r in subset)}/3 quedas, {sum(r['outcome'] == 'tie' for r in subset)}/3 empates.")
        if all(r["outcome"] == "tie" for r in relations if r["kind"] == "omission"):
            lines += ["", "A retirada explícita dos materiais não provocou queda de fidelidade nas três tarefas. Isso impede apresentar a nota global de fidelidade como comprovação de cumprimento dos sete requisitos.", "",
                      "Antes da coleta principal, recomenda-se revisar de forma versionada a operacionalização da fidelidade, exigindo verificação e evidência por requisito. Não mudar os outros critérios ou ampliar a escala apenas para produzir diferenças C1/C2. Manter este piloto e este diagnóstico intactos; uma versão revisada precisa ser testada separadamente, inclusive com casos novos que não participaram do ajuste.", ""]
    if write:
        (directory / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--model", choices=("gpt-5.4-mini-2026-03-17", "gpt-6.1-sol"))
    args = parser.parse_args()
    if args.summarize:
        report = summarize(args.output, model=args.model)
        print(json.dumps({k: report[k] for k in ("completed", "statuses", "outcomes", "usage")}))
    elif args.live:
        key = read_key()
        if not key:
            raise SystemExit("OpenAI credential absent")
        print(json.dumps(execute(args.output, key, model=args.model)))
    else:
        plan = build_plan(args.model)
        print(json.dumps({"planned": len(plan["jobs"]), "api_calls": 0}))
