"""Tests for the independent lesson-plan DOCX exporter."""

import io
import sys
import unittest
from pathlib import Path

from docx import Document


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from exporters import export_lesson_plan_docx  # noqa: E402
from pedagogical import lesson_plan_request_from_form  # noqa: E402


class LessonPlanExporterTests(unittest.TestCase):
    def setUp(self):
        self.request = lesson_plan_request_from_form({
            "subject": "Ciências",
            "topic": "Ciclo da água",
            "grade_level": "6º ano",
            "language": "pt-BR",
            "duration_minutes": 50,
            "llm_config": {"provider": "google", "model": "test-model"},
        })

    def test_export_returns_valid_localized_docx(self):
        content = "# Objetivos\n\n- Compreender a evaporação\n1. Observar o experimento"
        output = export_lesson_plan_docx(content, self.request)
        document = Document(io.BytesIO(output))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)

        self.assertTrue(output.startswith(b"PK"))
        self.assertIn("Ciências — Plano de Aula", text)
        self.assertIn("Tópico: Ciclo da água", text)
        self.assertIn("Duração: 50 minutos", text)
        self.assertIn("Compreender a evaporação", text)

    def test_empty_content_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty lesson plan"):
            export_lesson_plan_docx("   ", self.request)


if __name__ == "__main__":
    unittest.main()
