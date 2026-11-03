"""Unknown extraction and absent operational measurements keep their denominators."""
from pathlib import Path
import sys
import tempfile
import unittest
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from summarize_primary_metrics import distribution, summarize
from evaluate_pilot import evaluate
from experiment.pilot_runner import run_pilot


class PrimaryMetricSummaryTests(unittest.TestCase):
    def test_small_samples_do_not_invent_dispersion(self):
        self.assertIsNone(distribution([])["median"])
        self.assertIsNone(distribution([1])["iqr"])
        self.assertEqual(distribution([1, 2, 3, 4])["iqr"], 1.5)
        self.assertEqual(distribution([None, 5])["available"], 1)

    def test_simulated_partial_plan_keeps_unknowns_in_denominator(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            run_pilot(ROOT / "experiments/main_config.json", directory, max_jobs=4)
            metrics = evaluate(directory / "generations.jsonl", version="v2")
            (directory / "automatic_metrics.v2.json").write_text(json.dumps(metrics), encoding="utf-8")
            before = (directory / "generations.jsonl").read_bytes()
            report = summarize(directory)
            self.assertTrue(report["simulated"])
            self.assertIn("SIMULAÇÃO", (directory / "PRIMARY_METRICS_V2.md").read_text(encoding="utf-8"))
            self.assertEqual(len(report["groups"]), 78)
            for group in report["groups"]:
                for requirement in group["requirements"].values():
                    self.assertEqual(sum(requirement["counts"].values()), requirement["denominator"])
                    proportions = list(requirement["proportions"].values())
                    if requirement["denominator"]:
                        self.assertAlmostEqual(sum(proportions), 1)
                    else:
                        self.assertTrue(all(p is None for p in proportions))
            self.assertEqual((directory / "generations.jsonl").read_bytes(), before)
