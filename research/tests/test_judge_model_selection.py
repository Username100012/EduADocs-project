"""Integrity tests for the selected primary LLM judge configuration."""

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import JudgeConfiguration  # noqa: E402


class JudgeModelSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT_DIR / "experiments" / "judge_model_selection.v1.json"
        cls.selection = json.loads(path.read_text(encoding="utf-8"))

    def test_uses_exact_dated_snapshot_and_strict_schema(self):
        config = JudgeConfiguration.model_validate(
            self.selection["judge_configuration"], strict=True
        )
        self.assertEqual(config.model, "gpt-5.4-mini-2026-03-17")
        self.assertEqual(config.model_version, config.model)
        self.assertEqual(config.temperature, 0)
        self.assertIsNone(config.seed)
        self.assertEqual(config.response_format, "json_schema")
        self.assertTrue(config.provider_parameters["strict_schema"])

    def test_records_limited_independence(self):
        self.assertFalse(self.selection["exact_model_is_generator"])
        self.assertTrue(
            self.selection["provider_family_overlap_requires_separate_reporting"]
        )


if __name__ == "__main__":
    unittest.main()
