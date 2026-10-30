"""Architecture tests shared by notes, exercises and mind maps."""

import io
import sys
import unittest
from pathlib import Path

from docx import Document


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from exporters import export_exercise_list_docx, export_lecture_notes_docx, export_mind_map_docx  # noqa: E402
from pedagogical import exercise_list_request_from_form, lecture_notes_request_from_form, mind_map_request_from_form  # noqa: E402
from prompting import build_exercise_list_prompt, build_lecture_notes_prompt, build_mind_map_prompt  # noqa: E402


BASE = {
    "subject": "Ciências",
    "topic": "Ecossistemas",
    "grade_level": "6º ano",
    "language": "pt",
    "llm_config": {"provider": "google", "model": "test-model", "api_key": "secret"},
}


class RemainingModulesTests(unittest.TestCase):
    def _assert_module(self, request, prompt, exporter, version):
        self.assertEqual(prompt.template_version, version)
        self.assertNotIn("secret", request.model_dump_json())
        output = exporter("# Conteúdo\n- Item", request)
        document = Document(io.BytesIO(output))
        self.assertTrue(any("Conteúdo" in p.text for p in document.paragraphs))

    def test_lecture_notes(self):
        request = lecture_notes_request_from_form({**BASE, "detail_level": "Detalhado", "format_style": "Tópicos"})
        self._assert_module(request, build_lecture_notes_prompt(request), export_lecture_notes_docx, "lecture-notes-operational-v1.0.0")

    def test_exercise_list(self):
        request = exercise_list_request_from_form({**BASE, "num_questions": 8, "difficulty": "Médio", "question_types": ["Resposta curta"]})
        prompt = build_exercise_list_prompt(request)
        self.assertIn("Número de questões: 8", prompt.text)
        self._assert_module(request, prompt, export_exercise_list_docx, "exercise-list-operational-v1.0.0")

    def test_mind_map(self):
        request = mind_map_request_from_form({**BASE, "main_branches": 5, "depth_levels": 3})
        prompt = build_mind_map_prompt(request)
        self.assertIn("Ramos principais: 5", prompt.text)
        self._assert_module(request, prompt, export_mind_map_docx, "mind-map-operational-v1.0.0")


if __name__ == "__main__":
    unittest.main()
