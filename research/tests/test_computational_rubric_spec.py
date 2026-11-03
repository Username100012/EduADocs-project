"""Integrity tests for the frozen computational rubric specification."""

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
RUBRIC_PATH = ROOT_DIR / "experiments" / "computational_rubric.v1.json"


class ComputationalRubricSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))

    def test_declares_exactly_the_seven_controlled_requirements(self):
        self.assertEqual(self.rubric["requirement_count"], 7)
        self.assertEqual(
            self.rubric["requirements"],
            [
                "topic",
                "grade_level",
                "learning_objectives",
                "duration_minutes",
                "methodology",
                "materials",
                "assessment_strategy",
            ],
        )

    def test_primary_metric_formulas_are_frozen(self):
        metrics = self.rubric["primary_metrics"]
        self.assertEqual(metrics["requirement_compliance_score"], "count(score == 1) / 7")
        self.assertEqual(metrics["completeness_score"], "sum(score) / 7")
        self.assertEqual(metrics["omission_rate"], "count(score == 0) / 7")

    def test_does_not_use_llm_as_primary_judge(self):
        self.assertFalse(self.rubric["llm_as_primary_judge"])

    def test_repetitions_are_not_declared_independent(self):
        self.assertFalse(self.rubric["repetitions_are_independent"])
        self.assertEqual(self.rubric["statistical_unit"], "task")

    def test_failures_have_a_separate_primary_policy(self):
        policy = self.rubric["failure_policy"]
        self.assertEqual(
            policy["primary_analysis"],
            "exclude_from_structural_scores_and_report_separately",
        )
        self.assertTrue(policy["preserve_original_failure"])


if __name__ == "__main__":
    unittest.main()
