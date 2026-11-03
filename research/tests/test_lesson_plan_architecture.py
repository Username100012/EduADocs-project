"""Tests for lesson-plan parameterization and prompt construction."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from pedagogical import lesson_plan_request_from_form  # noqa: E402
from prompting import LESSON_PLAN_PROMPT_VERSION, build_lesson_plan_prompt  # noqa: E402


FORM_DATA = {
    "subject": "Ciências",
    "topic": "Ciclo da água",
    "grade_level": "6º ano",
    "language": "pt-BR",
    "duration_minutes": 50,
    "learning_objectives": "Compreender o ciclo da água",
    "materials": "Quadro e projetor",
    "methodology": "Aprendizagem baseada em problemas",
    "assessment_strategy": "Avaliação formativa",
    "lesson_flow": "Introdução, investigação e fechamento",
    "include_differentiation": True,
    "llm_config": {"provider": "google", "model": "test-model"},
}


class LessonPlanArchitectureTests(unittest.TestCase):
    def test_form_adapter_does_not_copy_credentials(self):
        data = {**FORM_DATA, "llm_config": {**FORM_DATA["llm_config"], "api_key": "secret"}}
        request = lesson_plan_request_from_form(data)
        self.assertNotIn("secret", request.model_dump_json())

    def test_prompt_is_deterministic_and_versioned(self):
        request = lesson_plan_request_from_form(FORM_DATA)
        first = build_lesson_plan_prompt(request)
        second = build_lesson_plan_prompt(request)
        self.assertEqual(first.text, second.text)
        self.assertEqual(first.sha256, second.sha256)
        self.assertEqual(first.template_version, LESSON_PLAN_PROMPT_VERSION)

    def test_language_is_an_explicit_instruction(self):
        request = lesson_plan_request_from_form(FORM_DATA)
        prompt = build_lesson_plan_prompt(request)
        self.assertIn("Idioma da resposta: pt-BR", prompt.text)
        self.assertIn("Produza todo o conteúdo em português", prompt.text)

    def test_prompt_contains_seven_experimental_requirements(self):
        request = lesson_plan_request_from_form(FORM_DATA)
        prompt = build_lesson_plan_prompt(request)
        self.assertEqual(len(prompt.expected_requirements), 7)
        for expected in (
            "Ciclo da água",
            "6º ano",
            "Compreender o ciclo da água",
            "50 minutos",
            "Aprendizagem baseada em problemas",
            "Quadro e projetor",
            "Avaliação formativa",
        ):
            self.assertIn(expected, prompt.text)


if __name__ == "__main__":
    unittest.main()
