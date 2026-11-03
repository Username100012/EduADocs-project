"""Formal information-equivalence checks for experimental conditions C1/C2."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    LessonPlanSemanticPayload,
    build_c1_prompt,
    build_c2_prompt,
)


class C1C2EquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.payload = LessonPlanSemanticPayload(
            topic="VALOR_UNICO_TOPICO",
            grade_level="VALOR_UNICO_NIVEL",
            learning_objectives="VALOR_UNICO_OBJETIVO",
            duration_minutes=937,
            methodology="VALOR_UNICO_METODOLOGIA",
            materials="VALOR_UNICO_MATERIAIS",
            assessment_strategy="VALOR_UNICO_AVALIACAO",
        )
        self.c1 = build_c1_prompt(self.payload)
        self.c2 = build_c2_prompt(self.payload)

    def test_payload_identity_is_recorded_in_both_conditions(self):
        self.assertEqual(self.c1.semantic_payload_hash, self.payload.semantic_hash)
        self.assertEqual(self.c2.semantic_payload_hash, self.payload.semantic_hash)
        self.assertEqual(self.c1.semantic_payload_hash, self.c2.semantic_payload_hash)

    def test_both_conditions_contain_the_same_seven_values_once(self):
        semantic_values = (
            self.payload.topic,
            self.payload.grade_level,
            self.payload.learning_objectives,
            str(self.payload.duration_minutes),
            self.payload.methodology,
            self.payload.materials,
            self.payload.assessment_strategy,
        )

        c1_occurrences = {value: self.c1.text.count(value) for value in semantic_values}
        c2_occurrences = {value: self.c2.text.count(value) for value in semantic_values}

        self.assertEqual(c1_occurrences, c2_occurrences)
        self.assertEqual(set(c1_occurrences.values()), {1})
        self.assertEqual(self.c1.expected_requirements, self.c2.expected_requirements)

    def test_structure_is_intentionally_different(self):
        self.assertNotEqual(self.c1.text, self.c2.text)
        self.assertNotEqual(self.c1.sha256, self.c2.sha256)

        self.assertNotIn("\n", self.c1.text)
        self.assertNotIn("PARÂMETROS PEDAGÓGICOS", self.c1.text)
        self.assertNotIn("- Tópico:", self.c1.text)

        self.assertIn("\n", self.c2.text)
        self.assertIn("PARÂMETROS PEDAGÓGICOS", self.c2.text)
        self.assertIn("- Tópico:", self.c2.text)

    def test_neither_condition_contains_operational_content(self):
        forbidden_terms = (
            "fluxo da aula",
            "diferenciação",
            "adaptações",
            "pré-requisitos",
            "atividades de extensão",
        )
        for term in forbidden_terms:
            self.assertNotIn(term, self.c1.text.lower())
            self.assertNotIn(term, self.c2.text.lower())


if __name__ == "__main__":
    unittest.main()
