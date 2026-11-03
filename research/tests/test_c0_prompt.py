"""Tests for the generic experimental condition C0."""

import sys
import unittest
from inspect import signature
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    C0_PROMPT_VERSION,
    LessonPlanSemanticPayload,
    build_c0_prompt,
)


class C0PromptTests(unittest.TestCase):
    def test_contains_only_material_type_and_topic(self):
        payload = LessonPlanSemanticPayload(
            topic="MARCADOR_TOPICO",
            grade_level="MARCADOR_NIVEL",
            learning_objectives="MARCADOR_OBJETIVO",
            duration_minutes=987,
            methodology="MARCADOR_METODOLOGIA",
            materials="MARCADOR_MATERIAIS",
            assessment_strategy="MARCADOR_AVALIACAO",
        )
        prompt = build_c0_prompt(payload.topic)

        self.assertEqual(
            prompt.text,
            "Elabore um plano de aula sobre o tema: MARCADOR_TOPICO.",
        )
        self.assertEqual(prompt.expected_requirements, ("topic",))

        forbidden_markers = (
            "MARCADOR_NIVEL",
            "MARCADOR_OBJETIVO",
            "987",
            "MARCADOR_METODOLOGIA",
            "MARCADOR_MATERIAIS",
            "MARCADOR_AVALIACAO",
            "MARCADOR_FLUXO",
            "MARCADOR_DIFERENCIACAO",
        )
        for marker in forbidden_markers:
            self.assertNotIn(marker, prompt.text)

    def test_signature_cannot_receive_other_requirements(self):
        self.assertEqual(tuple(signature(build_c0_prompt).parameters), ("topic",))

    def test_is_versioned_and_deterministic(self):
        first = build_c0_prompt("Ciclo da água")
        second = build_c0_prompt("Ciclo da água")

        self.assertEqual(first.template_version, C0_PROMPT_VERSION)
        self.assertEqual(first.text, second.text)
        self.assertEqual(first.sha256, second.sha256)

    def test_normalizes_outer_whitespace_only(self):
        prompt = build_c0_prompt("  Ciclo da água  ")
        self.assertEqual(
            prompt.text,
            "Elabore um plano de aula sobre o tema: Ciclo da água.",
        )

    def test_rejects_empty_topic(self):
        with self.assertRaisesRegex(ValueError, "non-empty topic"):
            build_c0_prompt("   ")


if __name__ == "__main__":
    unittest.main()
