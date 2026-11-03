"""Tests for the shared cross-module generation pipeline."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from application import execute_generation  # noqa: E402
from models import Provider  # noqa: E402
from pedagogical import lesson_plan_request_from_form  # noqa: E402
from prompting import build_lesson_plan_prompt  # noqa: E402
from providers import ProviderResponse  # noqa: E402


class MemorySink:
    def __init__(self):
        self.records = []

    def append(self, record):
        self.records.append(record)


class FakeGateway:
    def generate(self, request, prompt, connection_config):
        return ProviderResponse(
            content="# Conteúdo",
            provider=Provider.GOOGLE,
            model=request.model,
            latency_ms=5,
            input_tokens=10,
            output_tokens=20,
        )


class GenerationServiceTests(unittest.TestCase):
    def setUp(self):
        self.request = lesson_plan_request_from_form({
            "subject": "Ciências",
            "topic": "Água",
            "grade_level": "6º ano",
            "language": "pt",
            "duration_minutes": 50,
            "llm_config": {"provider": "google", "model": "test-model"},
        })
        self.prompt = build_lesson_plan_prompt(self.request)

    def test_success_uses_one_shared_pipeline(self):
        sink = MemorySink()
        outcome = execute_generation(
            self.request,
            self.prompt,
            {},
            lambda content, request: b"docx:" + content.encode(),
            gateway=FakeGateway(),
            record_sink=sink,
        )
        self.assertTrue(outcome.success)
        self.assertEqual(outcome.docx_file, "docx:# Conteúdo".encode())
        self.assertEqual(len(sink.records), 1)
        self.assertEqual(sink.records[0].status, "success")

    def test_export_failure_is_recorded(self):
        sink = MemorySink()

        def failing_exporter(content, request):
            raise RuntimeError("export failed")

        outcome = execute_generation(
            self.request,
            self.prompt,
            {},
            failing_exporter,
            gateway=FakeGateway(),
            record_sink=sink,
        )
        self.assertFalse(outcome.success)
        self.assertEqual(sink.records[0].status, "error")
        self.assertEqual(sink.records[0].raw_response, "# Conteúdo")


if __name__ == "__main__":
    unittest.main()
