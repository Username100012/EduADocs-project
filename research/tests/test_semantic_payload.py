"""Tests for the seven-requirement experimental semantic payload."""

import sys
import unittest
from pathlib import Path

from pydantic import ValidationError


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import LessonPlanSemanticPayload  # noqa: E402
from pedagogical import lesson_plan_request_from_form  # noqa: E402


COMPLETE_FORM = {
    "subject": "Ciências",
    "topic": "Ciclo da água",
    "grade_level": "6º ano",
    "language": "pt",
    "learning_objectives": "Compreender as etapas do ciclo da água",
    "duration_minutes": 50,
    "methodology": "Aprendizagem baseada em problemas",
    "materials": "Quadro, projetor e fichas",
    "assessment_strategy": "Avaliação formativa",
    "lesson_flow": "Aquecimento, exploração e fechamento",
    "include_differentiation": True,
    "llm_config": {"provider": "google", "model": "test-model"},
}


class SemanticPayloadTests(unittest.TestCase):
    def test_extracts_exactly_seven_requirements(self):
        request = lesson_plan_request_from_form(COMPLETE_FORM)
        payload = LessonPlanSemanticPayload.from_request(request)

        self.assertEqual(
            set(payload.model_dump()),
            {
                "topic",
                "grade_level",
                "learning_objectives",
                "duration_minutes",
                "methodology",
                "materials",
                "assessment_strategy",
            },
        )
        self.assertNotIn("lesson_flow", payload.model_dump())
        self.assertNotIn("include_differentiation", payload.model_dump())

    def test_incomplete_requirements_are_rejected(self):
        request = lesson_plan_request_from_form({
            **COMPLETE_FORM,
            "assessment_strategy": "",
        })
        with self.assertRaisesRegex(ValueError, "assessment_strategy"):
            LessonPlanSemanticPayload.from_request(request)

    def test_direct_operational_fields_are_forbidden(self):
        with self.assertRaises(ValidationError):
            LessonPlanSemanticPayload(
                topic="Ciclo da água",
                grade_level="6º ano",
                learning_objectives="Compreender o ciclo",
                duration_minutes=50,
                methodology="Problemas",
                materials="Quadro",
                assessment_strategy="Formativa",
                lesson_flow="Campo proibido",
            )

    def test_semantic_hash_is_stable(self):
        first = LessonPlanSemanticPayload.from_request(
            lesson_plan_request_from_form(COMPLETE_FORM)
        )
        second = LessonPlanSemanticPayload(**first.model_dump())
        self.assertEqual(first.canonical_json(), second.canonical_json())
        self.assertEqual(first.semantic_hash, second.semantic_hash)


if __name__ == "__main__":
    unittest.main()
