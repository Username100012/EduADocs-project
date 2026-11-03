"""Observable field extraction, deliberately separate from semantic judgments."""
import re

from experiment.automatic_metrics import normalize
from experiment.automatic_metrics_v2 import clean_line, duration_metrics

VERSION = "eduadocs-requirement-observations-v1"
LABELS = {
    "topic": r"(?:topico|tema)",
    "grade_level": r"(?:nivel(?: escolar| educacional| de ensino)?|publico-alvo|turma)",
    "learning_objectives": r"objetivos?(?: geral| gerais| especificos?| de aprendizagem)?",
    "duration_minutes": r"(?:duracao(?: total| da aula)?|carga horaria)",
    "methodology": r"metodologia(?: de ensino)?",
    "materials": r"(?:materiais(?: e recursos)?|recursos(?: e materiais)?)",
    "assessment_strategy": r"(?:estrategia de avaliacao|avaliacao(?: formativa| somativa| sumativa)?)",
}


def observe_requirements(text, target_minutes):
    """Detect labeled fields and preserve source lines; never infer compliance."""
    evidence = {name: [] for name in LABELS}
    labels = {name: [] for name in LABELS}
    active, fenced = None, False
    for number, original in enumerate(text.splitlines(), 1):
        if original.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            active = None
            continue
        if fenced:
            continue
        clean = clean_line(original)
        normalized = normalize(clean)
        found = next(((name, match) for name, pattern in LABELS.items()
                      if (match := re.match(r"^" + pattern + r"(?:\s*:|\s*$)", normalized))), None)
        if found:
            active, match = found
            labels[active].append({"line": number, "text": original})
            if normalized[match.end():].strip():
                evidence[active].append({"line": number, "text": original})
        elif clean and (original.lstrip().startswith("#") or
                        re.match(r"^\s*\*\*\d+(?:\.\d+)*[.)]?\s", original) or
                        re.match(r"^(?:referencias|conteudo|introducao|conclusao|dados gerais)\b", normalized) or
                        re.match(r"^[\w ]{1,40}:\s*", normalized)):
            active = None
        elif active and clean and not re.fullmatch(r"[-=]+", clean):
            evidence[active].append({"line": number, "text": original})
    return {"measurement_version": VERSION, "fields": {
                name: {"observation": "detected" if evidence[name] else "empty" if labels[name] else "not_detected",
                       "labels": labels[name], "evidence": evidence[name]} for name in LABELS},
            "duration": duration_metrics(text, target_minutes),
            "interpretation": "Labeled textual content only. Detected is not supported; not_detected is not a semantic omission. No aliases, negation heuristic or topic terms determine semantic status."}
