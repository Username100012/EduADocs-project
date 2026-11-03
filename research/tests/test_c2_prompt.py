"""Tests for experimental condition C2: structured seven-requirement prompt."""

import sys
import unittest
from inspect import signature
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    C2_PROMPT_VERSION,
    LessonPlanSemanticPayload,
    build_c2_prompt,
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


class C2PromptTests(unittest.TestCase):
    def test_contains_all_seven_semantic_values_once(self):
        payload = marked_payload()
        prompt = build_c2_prompt(payload)

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

    def test_uses_explicit_structured_blocks_and_fields(self):
        text = build_c2_prompt(marked_payload()).text

        self.assertIn("TAREFA\n", text)
        self.assertIn("PARÂMETROS PEDAGÓGICOS\n", text)
        self.assertIn("INSTRUÇÃO DE SAÍDA\n", text)
        self.assertIn("- Tópico:", text)
        self.assertIn("- Nível educacional:", text)
        self.assertIn("- Objetivo de aprendizagem:", text)
        self.assertIn("- Duração:", text)
        self.assertIn("- Metodologia:", text)
        self.assertIn("- Materiais e recursos:", text)
        self.assertIn("- Estratégia de avaliação:", text)

    def test_excludes_operational_requirements(self):
        text = build_c2_prompt(marked_payload()).text.lower()

        for forbidden in (
            "fluxo da aula",
            "diferenciação",
            "adaptações",
            "pré-requisitos",
            "atividades de extensão",
        ):
            self.assertNotIn(forbidden, text)

    def test_signature_accepts_only_semantic_payload(self):
        self.assertEqual(tuple(signature(build_c2_prompt).parameters), ("payload",))

    def test_is_versioned_and_deterministic(self):
        payload = marked_payload()
        first = build_c2_prompt(payload)
        second = build_c2_prompt(payload)

        self.assertEqual(first.template_version, C2_PROMPT_VERSION)
        self.assertEqual(first.text, second.text)
        self.assertEqual(first.sha256, second.sha256)


if __name__ == "__main__":
    unittest.main()
