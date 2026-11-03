"""Integrity tests for the versioned LLM-as-a-judge rubric."""

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
JUDGE_RUBRIC_PATH = ROOT_DIR / "experiments" / "llm_judge_rubric.v1.json"
COMPUTATIONAL_RUBRIC_PATH = ROOT_DIR / "experiments" / "computational_rubric.v1.json"


class LlmJudgeRubricSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rubric = json.loads(JUDGE_RUBRIC_PATH.read_text(encoding="utf-8"))
        cls.computational_rubric = json.loads(
            COMPUTATIONAL_RUBRIC_PATH.read_text(encoding="utf-8")
        )

    def test_is_secondary_and_pointwise(self):
        self.assertEqual(
            self.rubric["evaluation_role"], "secondary_automatic_metric"
        )
        self.assertEqual(self.rubric["evaluation_mode"], "pointwise")

    def test_has_four_distinct_semantic_criteria(self):
        criterion_ids = [criterion["id"] for criterion in self.rubric["criteria"]]
        self.assertEqual(
            criterion_ids,
            [
                "semantic_fidelity",
                "instructional_alignment",
                "grade_appropriateness",
                "coherence_feasibility",
            ],
        )

    def test_every_criterion_has_complete_four_point_anchors(self):
        for criterion in self.rubric["criteria"]:
            self.assertEqual(set(criterion["anchors"]), {"1", "2", "3", "4"})

    def test_blinding_repetition_and_structured_output_are_required(self):
        controls = self.rubric["controls"]
        self.assertTrue(controls["blind_condition"])
        self.assertTrue(controls["blind_generator_identity"])
        self.assertEqual(controls["temperature"], 0)
        self.assertEqual(controls["judgments_per_response"], 3)
        self.assertEqual(self.rubric["output_contract"]["format"], "json")

    def test_does_not_claim_human_or_pedagogical_ground_truth(self):
        excluded = set(self.rubric["excluded_claims"])
        self.assertIn("human_judgment", excluded)
        self.assertIn("proven_pedagogical_quality", excluded)
        self.assertFalse(
            self.computational_rubric["llm_judge"]["human_ground_truth_claimed"]
        )
        self.assertFalse(self.computational_rubric["llm_as_primary_judge"])

    def test_declares_bias_audit_tests(self):
        tests = set(self.rubric["metamorphic_tests"])
        self.assertIn("pairwise_position_invariance", tests)
        self.assertIn("verbosity_non_improvement", tests)
        self.assertIn("controlled_omission_non_improvement", tests)


if __name__ == "__main__":
    unittest.main()
