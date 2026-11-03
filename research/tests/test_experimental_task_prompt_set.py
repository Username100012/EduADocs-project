"""Tests for the validated C0/C1/C2 bundle of one experimental task."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    ExperimentalTaskPromptSet,
    LessonPlanSemanticPayload,
    build_experimental_task_prompt_set,
)


def payload() -> LessonPlanSemanticPayload:
    return LessonPlanSemanticPayload(
        topic="Ciclo da água",
        grade_level="6º ano",
        learning_objectives="Compreender as etapas do ciclo da água",
        duration_minutes=50,
        methodology="Aprendizagem baseada em problemas",
        materials="Quadro, projetor e fichas",
        assessment_strategy="Avaliação formativa",
    )


class ExperimentalTaskPromptSetTests(unittest.TestCase):
    def test_builds_three_conditions_in_canonical_order(self):
        task = build_experimental_task_prompt_set("task-001", payload())

        self.assertEqual(tuple(task.conditions), ("c0", "c1", "c2"))
        self.assertEqual(task.c0.expected_requirements, ("topic",))
        self.assertEqual(task.c1.semantic_payload_hash, task.payload.semantic_hash)
        self.assertEqual(task.c2.semantic_payload_hash, task.payload.semantic_hash)
        self.assertNotEqual(task.c1.sha256, task.c2.sha256)

    def test_manifest_contains_prompts_versions_and_hashes(self):
        task = build_experimental_task_prompt_set("task-001", payload())
        manifest = task.to_manifest_dict()

        self.assertEqual(manifest["task_id"], "task-001")
        self.assertEqual(manifest["semantic_payload_hash"], task.payload.semantic_hash)
        self.assertEqual(tuple(manifest["conditions"]), ("c0", "c1", "c2"))
        for name, prompt in task.conditions.items():
            entry = manifest["conditions"][name]
            self.assertEqual(entry["text"], prompt.text)
            self.assertEqual(entry["template_version"], prompt.template_version)
            self.assertEqual(entry["prompt_sha256"], prompt.sha256)

    def test_build_is_deterministic(self):
        first = build_experimental_task_prompt_set("task-001", payload())
        second = build_experimental_task_prompt_set("task-001", payload())
        self.assertEqual(first.to_manifest_dict(), second.to_manifest_dict())

    def test_rejects_empty_task_id(self):
        with self.assertRaisesRegex(ValueError, "task_id"):
            build_experimental_task_prompt_set("   ", payload())

    def test_rejects_c1_from_another_payload(self):
        task = build_experimental_task_prompt_set("task-001", payload())
        other_payload = payload().model_copy(update={"topic": "Fotossíntese"})
        foreign = build_experimental_task_prompt_set("task-002", other_payload)

        with self.assertRaisesRegex(ValueError, "C1 was not derived"):
            ExperimentalTaskPromptSet(
                task_id=task.task_id,
                payload=task.payload,
                c0=task.c0,
                c1=foreign.c1,
                c2=task.c2,
            )

    def test_rejects_tampered_condition_version(self):
        task = build_experimental_task_prompt_set("task-001", payload())
        tampered_c0 = replace(task.c0, template_version="invalid-version")

        with self.assertRaisesRegex(ValueError, "C0 template version"):
            ExperimentalTaskPromptSet(
                task_id=task.task_id,
                payload=task.payload,
                c0=tampered_c0,
                c1=task.c1,
                c2=task.c2,
            )


if __name__ == "__main__":
    unittest.main()
