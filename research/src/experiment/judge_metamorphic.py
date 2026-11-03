"""Build controlled synthetic pairs without invoking a judge."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

from experiment.semantic_payload import LessonPlanSemanticPayload


@dataclass(frozen=True)
class MetamorphicPair:
    case_id: str
    kind: str
    payload: LessonPlanSemanticPayload
    baseline: str
    variant: str
    criterion: str
    operator: str


def load_metamorphic_pairs(path: Path) -> tuple[MetamorphicPair, ...]:
    spec = json.loads(path.read_text(encoding="utf-8"))
    pairs = []
    for seed in spec["seeds"]:
        payload = LessonPlanSemanticPayload.model_validate(seed["payload"])
        sections = seed["sections"]
        baseline = "\n".join(sections)
        variants = {
            "consistency": baseline,
            "verbosity": baseline + "\n" + spec["verbosity_suffix"],
            "omission": "\n".join(sections[:2] + sections[3:]),
            "misalignment": "\n".join(sections[:-1] + [seed["misaligned_assessment"]]),
        }
        for relation in spec["relations"]:
            kind = relation["kind"]
            pairs.append(MetamorphicPair(
                case_id=f"{seed['id']}-{kind}", kind=kind, payload=payload,
                baseline=baseline, variant=variants[kind],
                criterion=relation["criterion"], operator=relation["operator"],
            ))
    return tuple(pairs)


def metamorphic_suite_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()
