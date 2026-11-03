"""Versioned formatting-tolerant lexical proxies; v1 remains untouched."""

import re

from experiment.automatic_metrics import normalize

METRICS_VERSION = "eduadocs-textual-proxies-v2"


def clean_line(text):
    text = re.sub(r"[*_`]+", "", text).strip()
    text = re.sub(r"^#{1,6}\s*", "", text)
    text = re.sub(r"^[-+•]\s+", "", text)
    return re.sub(r"^(?:\d+(?:\.\d+)+[.)]?|\d+[.)])\s+", "", text).strip()


LABELS = {
    "objective": r"objetivos?(?: geral| gerais| especificos?| de aprendizagem)?",
    "materials": r"(?:materiais(?: e recursos)?|recursos(?: e materiais)?)",
    "methodology": r"metodologia(?: de ensino)?",
    "assessment": r"(?:estrategia de avaliacao|avaliacao(?: formativa| somativa| sumativa)?)",
}
BOUNDARIES = r"(?:titulo|plano de aula|dados gerais|disciplina|nivel(?: educacional| de ensino)?|formacao|duracao(?: total| da aula)?|carga horaria|cronograma(?: da aula)?|conteudo(?: programatico| da aula)?|estrutura(?: do plano(?: de aula)?)?|introducao|conclusao|referencias(?: opcionais)?|fim do plano)"


def lines_with_sections(text):
    section = None
    fenced = False
    result = []
    for number, original in enumerate(text.splitlines(), 1):
        if original.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        cleaned = clean_line(original)
        n = normalize(cleaned)
        if not fenced:
            matched = next((name for name, label in LABELS.items()
                            if re.match(r"^(?:" + label + r")(?:\s*:|\s*$)", n)), None)
            if matched:
                section = matched
            elif (re.match(r"^" + BOUNDARIES + r"(?:\s*:|\s*\(|\s*$)", n)
                  or (original.lstrip().startswith("#") and cleaned)
                  or re.match(r"^\s*\*\*\d+(?:\.\d+)*[.)]?\s", original)):
                section = None
        result.append((number, original, section))
    return result


def group_presence(lines, groups, *, section=None):
    eligible = [line for line in lines if section is None or line[2] == section]
    found, ambiguous = [], False
    for aliases in groups:
        evidence = []
        for number, original, _ in eligible:
            n = normalize(re.sub(r"[*_`]+", "", original))
            for alias in aliases:
                a = normalize(alias)
                for match in re.finditer(r"(?<!\w)" + re.escape(a) + r"(?!\w)", n):
                    prefix = n[max(0, match.start() - 60):match.start()]
                    if a in {"funcional", "funcionais"} and re.search(r"nao\s+$", prefix):
                        continue
                    # Treat the domain term as a category, not an instruction
                    # negation, while preserving other negation in the prefix.
                    prefix = re.sub(r"\bnao\s+(?=funciona(?:l|is)\b)", "", prefix)
                    uncertain = bool(re.search(r"\b(?:nao|sem|exceto|evitar)\b", prefix))
                    ambiguous |= uncertain
                    evidence.append({"line": number, "text": original,
                                     "alias": alias, "ambiguous_context": uncertain})
        found.append({"aliases": aliases, "evidence": evidence,
                      "positive_match": any(not e["ambiguous_context"] for e in evidence)})
    positive = all(g["positive_match"] for g in found)
    return {"present": True if positive else None if ambiguous or not eligible else False,
            "groups": found, "section_required": section,
            "interpretation": "explicit_textual_evidence_only"}


def duration_metrics(text, target):
    lines = text.splitlines()
    declared, unresolved = [], []
    unit = r"(\d+(?:[.,]\d+)?)\s*(horas?|h|minutos?|min)\b"
    for index, original in enumerate(lines):
        n = normalize(clean_line(original))
        label = re.match(r"^(?:duracao(?: total| da aula)?|carga horaria)\s*(?::|$)", n)
        if not label:
            continue
        segment = n[label.end():].strip()
        source = original
        if not segment:
            following = next((j for j in range(index + 1, len(lines)) if lines[j].strip()), None)
            if following is not None:
                segment = normalize(clean_line(lines[following]))
                source += "\n" + "\n".join(lines[index + 1:following + 1])
        parts = list(re.finditer(unit, segment))
        multiple = re.search(r"\b(\d+)\s+aulas?\b", segment)
        starts_numeric = re.match(r"^\d", segment)
        if (not parts or not starts_numeric or (multiple and "cada" not in segment)
                or (multiple and re.search(r"\btotal\b", segment))):
            unresolved.append({"line": index + 1, "text": source})
            continue
        minutes = sum(float(m[1].replace(",", ".")) * (60 if m[2].startswith("h") else 1) for m in parts)
        if multiple:
            minutes *= int(multiple[1])
        declared.append({"minutes": minutes, "line": index + 1, "text": source})
    intervals = []
    for match in re.finditer(r"\b(\d{1,2}):([0-5]\d)\s*[-–—]\s*(\d{1,2}):([0-5]\d)\b", text):
        intervals.append({"start": int(match[1]) * 60 + int(match[2]),
                          "end": int(match[3]) * 60 + int(match[4]), "text": match[0]})
    consecutive = bool(intervals) and all(i["end"] > i["start"] for i in intervals)
    consecutive = consecutive and all(a["end"] == b["start"] for a, b in zip(intervals, intervals[1:]))
    schedule = sum(i["end"] - i["start"] for i in intervals) if consecutive else None
    values = [d["minutes"] for d in declared]
    known = values + ([schedule] if schedule is not None else [])
    internal = len(set(known)) > 1 if len(known) > 1 else None
    return {"target_minutes": target, "declared": declared, "unresolved_declarations": unresolved,
            "declared_matches_target": all(v == target for v in values) if values else None,
            "clock_intervals": intervals, "clock_schedule_minutes": schedule,
            "schedule_matches_target": schedule == target if schedule is not None else None,
            "target_mismatch_detected": any(v != target for v in known) if known else None,
            "internal_inconsistency_detected": internal,
            "warning": "Only explicit numeric declarations and contiguous HH:MM intervals; step durations are not summed. No detected inconsistency is not proof of consistency."}


def evaluate_text(text, task):
    if not text or not text.strip():
        return {"metrics_version": METRICS_VERSION, "status": "empty_response", "requirements": None, "word_count": 0}
    lines = lines_with_sections(text)
    a = task["textual_evidence"]
    topic = a["topic_concept_groups"]
    requirements = {
        "topic": group_presence(lines, topic),
        "grade_level": group_presence(lines, [a["grade_aliases"]]),
        "learning_objectives": group_presence(lines, [a["objective_verbs"]] + topic, section="objective"),
        "duration_minutes": duration_metrics(text, task["payload"]["duration_minutes"]),
        "methodology": group_presence(lines, [a["methodology_aliases"]], section="methodology"),
        "materials": group_presence(lines, a["required_resource_groups"], section="materials"),
        "assessment_strategy": group_presence(lines, a["assessment_action_groups"], section="assessment"),
    }
    requirements["grade_level"]["mixed_school_levels_mentioned"] = bool(re.search(r"ensino medio|fundamental", normalize(text)))
    return {"metrics_version": METRICS_VERSION, "status": "text_available",
            "word_count": len(re.findall(r"\b\w+(?:[-']\w+)*\b", text)), "requirements": requirements,
            "limitations": ["Lexical proxies, not semantic or pedagogical validation.",
                            "Only documented label and formatting variants are supported; no universal invariance.",
                            "Mixed-level flag is a mention heuristic, not audience or age suitability.",
                            "Negation remains heuristic; unknown sections and paraphrases can cause missing evidence."]}
