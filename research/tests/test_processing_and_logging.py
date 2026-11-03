"""Tests for response preservation and reproducible JSONL records."""

import json
import sys
import tempfile
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import ExecutionLogger, ExecutionRecord  # noqa: E402
from processing import process_response  # noqa: E402


class ProcessingAndLoggingTests(unittest.TestCase):
    def test_processing_preserves_raw_content(self):
        raw = "<think>private reasoning</think>\n\n# Resultado"
        processed = process_response(raw)
        self.assertEqual(processed.raw_content, raw)
        self.assertEqual(processed.content, "# Resultado")
        self.assertIn("reasoning_blocks_removed", processed.warnings)

    def test_execution_record_is_appended_as_jsonl(self):
        record = ExecutionRecord(
            execution_id="test-id",
            status="success",
            request={"provider": "google"},
            prompt={"template_version": "v1", "sha256": "abc"},
            provider_response={"latency_ms": 10, "input_tokens": 3},
            raw_response="# Raw",
            processed_response="# Raw",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "executions.jsonl"
            ExecutionLogger(path).append(record)
            data = json.loads(path.read_text(encoding="utf-8").strip())
        self.assertEqual(data["execution_id"], "test-id")
        self.assertEqual(data["schema_version"], "eduadocs-execution-v1.0.0")

    def test_record_rejects_undeclared_credentials(self):
        with self.assertRaises(Exception):
            ExecutionRecord(
                execution_id="test-id",
                status="success",
                request={},
                prompt={},
                provider_response={},
                raw_response="raw",
                processed_response="processed",
                api_key="must-not-be-recorded",
            )


if __name__ == "__main__":
    unittest.main()
