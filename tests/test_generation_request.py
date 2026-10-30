"""Tests for the provider-independent generation request models."""

import sys
import unittest
from pathlib import Path

from pydantic import ValidationError


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from models.generation_request import (  # noqa: E402
    DocumentType,
    ExperimentalCondition,
    GenerationRequest,
    LessonPlanParameters,
    Provider,
)


def complete_lesson_plan_parameters() -> LessonPlanParameters:
    return LessonPlanParameters(
        learning_objectives="Compreender o ciclo da água",
        duration_minutes=50,
        methodology="Aprendizagem baseada em problemas",
        materials="Quadro, projetor e fichas",
        assessment_strategy="Avaliação formativa durante a atividade",
        lesson_flow="Introdução, investigação e fechamento",
        include_differentiation=True,
    )


class GenerationRequestTests(unittest.TestCase):
    def test_operational_request_is_serializable(self):
        request = GenerationRequest(
            document_type=DocumentType.LESSON_PLAN,
            subject="Ciências",
            topic="Ciclo da água",
            grade_level="6º ano",
            language="pt-BR",
            provider=Provider.GOOGLE,
            model="gemini-test",
            pedagogical_parameters=complete_lesson_plan_parameters(),
        )

        serialized = request.model_dump_json()

        self.assertIn('"document_type":"lesson_plan"', serialized)
        self.assertIn('"provider":"google"', serialized)
        self.assertNotIn("api_key", serialized)

    def test_c2_requires_all_seven_requirements(self):
        with self.assertRaises(ValidationError) as context:
            GenerationRequest(
                document_type=DocumentType.LESSON_PLAN,
                subject="Ciências",
                topic="Ciclo da água",
                grade_level="6º ano",
                provider=Provider.OPENAI,
                model="test-model",
                experimental_condition=ExperimentalCondition.C2_STRUCTURED,
                pedagogical_parameters=LessonPlanParameters(duration_minutes=50),
            )

        self.assertIn("missing lesson-plan fields", str(context.exception))

    def test_c0_accepts_parameters_absent_from_generic_prompt(self):
        request = GenerationRequest(
            document_type=DocumentType.LESSON_PLAN,
            subject="Ciências",
            topic="Ciclo da água",
            grade_level="6º ano",
            provider=Provider.OLLAMA,
            model="local-test",
            experimental_condition=ExperimentalCondition.C0_GENERIC,
            pedagogical_parameters=LessonPlanParameters(),
        )

        self.assertEqual(request.experimental_condition, ExperimentalCondition.C0_GENERIC)

    def test_api_credentials_are_rejected(self):
        with self.assertRaises(ValidationError):
            GenerationRequest(
                document_type=DocumentType.LESSON_PLAN,
                subject="Ciências",
                topic="Ciclo da água",
                grade_level="6º ano",
                provider=Provider.GOOGLE,
                model="gemini-test",
                pedagogical_parameters=complete_lesson_plan_parameters(),
                api_key="must-not-be-stored",
            )

    def test_blank_optional_text_is_normalized(self):
        parameters = LessonPlanParameters(materials="   ")
        self.assertIsNone(parameters.materials)


if __name__ == "__main__":
    unittest.main()
