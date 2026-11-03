"""Tests for experimental condition C1: free text with seven requirements."""

import sys
import unittest
from inspect import signature
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    C1_PROMPT_VERSION,
    LessonPlanSemanticPayload,
    build_c1_prompt,
)


def marked_payload() -> LessonPlanSemanticPayload:
    return LessonPlanSemanticPayload(
        topic="MARCADOR_TOPICO",
        grade_level="MARCADOR_NIVEL",
        learning_objectives="MARCADOR_OBJETIVO",
        duration_minutes=987,
        methodology="MARCADOR_METODOLOGIA",
        materials="MARCADOR_MATERIAIS",
        assessment_strategy="MARCADOR_AVALIACAO",
    )


class C1PromptTests(unittest.TestCase):
    def test_contains_all_seven_semantic_values(self):
        payload = marked_payload()
        prompt = build_c1_prompt(payload)

        for value in (
            payload.topic,
            payload.grade_level,
            payload.learning_objectives,
            str(payload.duration_minutes),
            payload.methodology,
            payload.materials,
            payload.assessment_strategy,
        ):
            self.assertEqual(prompt.text.count(value), 1)

        self.assertEqual(
            prompt.expected_requirements,
            (
                "topic",
                "grade_level",
                "learning_objectives",
                "duration_minutes",
                "methodology",
                "materials",
                "assessment_strategy",
            ),
        )

    def test_is_one_free_text_paragraph_without_field_layout(self):
        prompt = build_c1_prompt(marked_payload())

        self.assertNotIn("\n", prompt.text)
        self.assertNotIn("- ", prompt.text)
        self.assertNotIn("#", prompt.text)
        self.assertNotIn("Tópico:", prompt.text)
        self.assertNotIn("Metodologia:", prompt.text)

    def test_excludes_operational_requirements(self):
        prompt = build_c1_prompt(marked_payload())

        for forbidden in (
            "fluxo da aula",
            "diferenciação",
            "adaptações",
            "pré-requisitos",
            "atividades de extensão",
        ):
            self.assertNotIn(forbidden, prompt.text.lower())

    def test_signature_accepts_only_semantic_payload(self):
        self.assertEqual(tuple(signature(build_c1_prompt).parameters), ("payload",))

    def test_is_versioned_and_deterministic(self):
        payload = marked_payload()
        first = build_c1_prompt(payload)
        second = build_c1_prompt(payload)

        self.assertEqual(first.template_version, C1_PROMPT_VERSION)
        self.assertEqual(first.text, second.text)
        self.assertEqual(first.sha256, second.sha256)


if __name__ == "__main__":
    unittest.main()
