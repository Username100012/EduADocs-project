"""Conservative textual proxies; not semantic or pedagogical validation."""

import re
import unicodedata


METRICS_VERSION = "eduadocs-textual-proxies-v1"


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold())
                   if not unicodedata.combining(c))


def lines_with_sections(text):
    section = None
    output = []
    for number, original in enumerate(text.splitlines(), 1):
        clean = re.sub(r"[*#_]", "", original).strip()
        clean = re.sub(r"^\d+[.)]\s*", "", clean)
        n = normalize(clean)
        headings = {"objective": r"objetivos?(?: de aprendizagem)?\s*:",
                    "materials": r"(?:materiais(?: e recursos)?|recursos)\s*:",
                    "methodology": r"metodologia\s*:",
                    "assessment": r"(?:estrategia de avaliacao|avaliacao(?: formativa| somativa| sumativa)?)\s*:"}
        matched = next((name for name, pattern in headings.items() if re.match(pattern, n)), None)
        if matched:
            section = matched
        elif clean and (original.lstrip().startswith("#") or
                        re.match(r"^\s*\*\*\d+[.)]", original) or
                        re.match(r"^(?:titulo|nivel educacional|duracao|cronograma(?: da aula)?|referencias|fim do plano)\b", n)):
            section = None
        output.append((number, original, section))
    return output


def group_presence(lines, groups, *, section=None):
    eligible = [line for line in lines if section is None or line[2] == section]
    found, ambiguous = [], False
    for aliases in groups:
        evidence = []
        for number, original, _ in eligible:
            n = normalize(original)
            for alias in aliases:
                a = normalize(alias)
                for match in re.finditer(r"(?<!\w)" + re.escape(a) + r"(?!\w)", n):
                    prefix = n[max(0, match.start() - 60):match.start()]
                    # Avoid treating "não funcionais" as the positive category "funcionais".
                    if a in {"funcional", "funcionais"} and re.search(r"nao\s+$", prefix):
                        continue
                    uncertain = bool(re.search(r"\b(?:nao|sem|exceto|evitar)\b", prefix))
                    ambiguous |= uncertain
                    evidence.append({"line": number, "text": original,
                                     "alias": alias, "ambiguous_context": uncertain})
        found.append({"aliases": aliases, "evidence": evidence,
                      "positive_match": any(not e["ambiguous_context"] for e in evidence)})
    present = all(group["positive_match"] for group in found)
    return {"present": True if present else None if ambiguous or not eligible else False,
            "groups": found, "section_required": section,
            "interpretation": "explicit_textual_evidence_only"}


def duration_metrics(text, target):
    # Parse only explicit numeric durations and consecutive clock intervals.
    cleaned = re.sub(r"[*#_]", "", text)
    lines = cleaned.splitlines()
    declared = []
    number = r"\d+(?:[.,]\d+)?"
    unit = rf"({number})\s*(horas?|h|minutos?|min)\b"
    for index, line in enumerate(lines):
        n = normalize(line)
        if re.search(r"\bduracao(?:\s+total)?\s*:", n):
            segment = n.split(":", 1)[1]
            if not segment.strip() and index + 1 < len(lines):
                segment = normalize(lines[index + 1])
            matches = list(re.finditer(unit, segment))
            if matches:
                value = sum(float(m[1].replace(",", ".")) * (60 if m[2].startswith("h") else 1)
                            for m in matches)
                declared.append({"minutes": value, "line": index + 1,
                                 "text": "\n".join(lines[index:index + 2])})
    intervals = []
    pattern = r"\b(\d{1,2}):([0-5]\d)\s*[-–—]\s*(\d{1,2}):([0-5]\d)\b"
    for m in re.finditer(pattern, cleaned):
        start, end = int(m[1]) * 60 + int(m[2]), int(m[3]) * 60 + int(m[4])
        intervals.append({"start": start, "end": end, "text": m[0]})
    consecutive = bool(intervals) and all(i["end"] > i["start"] for i in intervals)
    consecutive = consecutive and all(a["end"] == b["start"] for a, b in zip(intervals, intervals[1:]))
    total = sum(i["end"] - i["start"] for i in intervals) if consecutive else None
    declarations = [d["minutes"] for d in declared]
    contradictions = any(d != target for d in declarations) or (total is not None and total != target)
    contradictions |= len(set(declarations)) > 1
    return {"target_minutes": target, "declared": declared,
            "declared_matches_target": all(d == target for d in declarations) if declarations else None,
            "clock_intervals": intervals, "clock_schedule_minutes": total,
            "schedule_matches_target": total == target if total is not None else None,
            "detected_contradiction": bool(contradictions),
            "warning": "Only explicit numeric declarations and contiguous HH:MM intervals are parsed; no inference from absence. Clock intervals are interpreted as lesson minutes."}


def evaluate_text(text, task):
    if not text or not text.strip():
        return {"metrics_version": METRICS_VERSION, "status": "empty_response",
                "requirements": None, "word_count": 0}
    lines = lines_with_sections(text)
    anchors = task["textual_evidence"]
    topic = anchors["topic_concept_groups"]
    duration = duration_metrics(text, task["payload"]["duration_minutes"])
    return {
        "metrics_version": METRICS_VERSION, "status": "text_available",
        "word_count": len(re.findall(r"\b\w+(?:[-']\w+)*\b", text)),
        "requirements": {
            "topic": group_presence(lines, topic),
            "grade_level": group_presence(lines, [anchors["grade_aliases"]]),
            "learning_objectives": group_presence(lines, [anchors["objective_verbs"]] + topic, section="objective"),
            "duration_minutes": duration,
            "methodology": group_presence(lines, [anchors["methodology_aliases"]], section="methodology"),
            "materials": group_presence(lines, anchors["required_resource_groups"], section="materials"),
            "assessment_strategy": group_presence(lines, anchors["assessment_action_groups"], section="assessment"),
        },
        "limitations": ["Not a semantic compliance score or factual validation.",
                        "Missing aliases or unrecognized headings can cause false negatives or nulls.",
                        "Negation detection is conservative and heuristic; language suitability is not evaluated."],
    }


def operational_metrics(response):
    """Keep absent provider measurements missing; do not fabricate cost."""
    return {key: response.get(key) for key in
            ("latency_ms", "input_tokens", "output_tokens", "finish_reason")}
