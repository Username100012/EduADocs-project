"""Simulation must expose failures and constant judges, not just pass cases."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.metamorphic_runner import run_simulation


class MetamorphicRunnerTests(unittest.TestCase):
    def run_case(self, scenario):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name) / "run"
        report = run_simulation(
            ROOT / "experiments/judge_metamorphic_cases.v1.json", output, scenario=scenario
        )
        rows = [json.loads(line) for line in (output / "attempts.jsonl").read_text().splitlines()]
        return report, rows, output

    def test_expected_relations_and_identical_duplicate_prompts(self):
        report, rows, output = self.run_case("expected")
        self.assertEqual(report["planned_judgments"], 72)
        self.assertEqual(report["attempts"], 72)
        self.assertTrue(report["simulated"])
        self.assertEqual(len({r["record_id"] for r in rows}), 72)
        for group in report["groups"].values():
            self.assertEqual(group["satisfaction_rate"], 1)
        duplicate = [r for r in rows if r["case_id"] == "science-consistency"]
        self.assertEqual(len({r["prompt_hash"] for r in duplicate}), 1)
        self.assertNotIn("condition", rows[0])
        with self.assertRaises(FileExistsError):
            run_simulation(ROOT / "experiments/judge_metamorphic_cases.v1.json", output)

    def test_constant_judge_is_visible_as_ties_despite_passing_relations(self):
        report, _, _ = self.run_case("constant")
        self.assertEqual(report["groups"]["omission"]["criterion_direction_counts"], {"tie": 3})

    def test_violations_are_reported(self):
        report, _, _ = self.run_case("violations")
        for group in report["groups"].values():
            self.assertEqual(group["satisfaction_rate"], 0)

    def test_incomplete_pairs_preserve_both_failed_attempts(self):
        report, _, _ = self.run_case("incomplete")
        self.assertEqual(report["attempts"], 75)
        self.assertEqual(report["failed_attempts"], 6)
        self.assertEqual(report["groups"]["consistency"]["incomplete_pairs"], 1)
        self.assertEqual(report["groups"]["consistency"]["complete_pairs"], 2)
