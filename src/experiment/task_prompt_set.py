"""Validated bundle of C0, C1 and C2 prompts for one experimental task."""

from dataclasses import dataclass
from typing import Any

from experiment.prompt_conditions import (
    C0_PROMPT_VERSION,
    C1_PROMPT_VERSION,
    C2_PROMPT_VERSION,
    EXPERIMENTAL_REQUIREMENTS,
    build_c0_prompt,
    build_c1_prompt,
    build_c2_prompt,
)
from experiment.semantic_payload import LessonPlanSemanticPayload
from prompting import PromptArtifact


@dataclass(frozen=True, slots=True)
class ExperimentalTaskPromptSet:
    """The three validated conditions derived for one lesson-plan task."""

    task_id: str
    payload: LessonPlanSemanticPayload
    c0: PromptArtifact
    c1: PromptArtifact
    c2: PromptArtifact

    def __post_init__(self) -> None:
        normalized_id = self.task_id.strip()
        if not normalized_id:
            raise ValueError("task_id must not be empty")
        object.__setattr__(self, "task_id", normalized_id)

        if self.c0.template_version != C0_PROMPT_VERSION:
            raise ValueError("C0 template version does not match the protocol")
        if self.c1.template_version != C1_PROMPT_VERSION:
            raise ValueError("C1 template version does not match the protocol")
        if self.c2.template_version != C2_PROMPT_VERSION:
            raise ValueError("C2 template version does not match the protocol")

        if self.c0.expected_requirements != ("topic",):
            raise ValueError("C0 must contain only the topic requirement")
        if self.c1.expected_requirements != EXPERIMENTAL_REQUIREMENTS:
            raise ValueError("C1 requirements do not match the experimental protocol")
        if self.c2.expected_requirements != EXPERIMENTAL_REQUIREMENTS:
            raise ValueError("C2 requirements do not match the experimental protocol")

        expected_hash = self.payload.semantic_hash
        if self.c1.semantic_payload_hash != expected_hash:
            raise ValueError("C1 was not derived from this task payload")
        if self.c2.semantic_payload_hash != expected_hash:
            raise ValueError("C2 was not derived from this task payload")
        if self.c1.sha256 == self.c2.sha256:
            raise ValueError("C1 and C2 must have different textual structures")

    @property
    def conditions(self) -> dict[str, PromptArtifact]:
        """Return conditions in their canonical experimental order."""

        return {"c0": self.c0, "c1": self.c1, "c2": self.c2}

    def to_manifest_dict(self) -> dict[str, Any]:
        """Return deterministic metadata for a future experiment manifest."""

        return {
            "task_id": self.task_id,
            "semantic_payload": self.payload.model_dump(mode="json"),
            "semantic_payload_hash": self.payload.semantic_hash,
            "conditions": {
                name: {
                    "text": prompt.text,
                    "template_version": prompt.template_version,
                    "prompt_sha256": prompt.sha256,
                    "semantic_payload_hash": prompt.semantic_payload_hash,
                    "expected_requirements": list(prompt.expected_requirements),
                }
                for name, prompt in self.conditions.items()
            },
        }


def build_experimental_task_prompt_set(
    task_id: str,
    payload: LessonPlanSemanticPayload,
) -> ExperimentalTaskPromptSet:
    """Build and validate all conditions without invoking a language model."""

    return ExperimentalTaskPromptSet(
        task_id=task_id,
        payload=payload,
        c0=build_c0_prompt(payload.topic),
        c1=build_c1_prompt(payload),
        c2=build_c2_prompt(payload),
    )
