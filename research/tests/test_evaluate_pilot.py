"""Saved-log analysis must preserve failures, truncations and simulation labels."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.pilot_runner import run_pilot

spec = importlib.util.spec_from_file_location("evaluate_pilot", ROOT / "scripts/evaluate_pilot.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SavedPilotMetricsTests(unittest.TestCase):
    def test_v2_is_explicit_and_duplicate_results_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            run_pilot(ROOT / "experiments/pilot_config.json", directory,
                      generator_ids=["qwen3"], max_jobs=1)
            path = directory / "generations.jsonl"
            report = module.evaluate(path, version="v2")
            self.assertEqual(report["metrics_version"], "eduadocs-textual-proxies-v2")
            self.assertNotIn("detected_duration_contradictions", report["groups"][0])
            with self.assertRaises(ValueError):
                module.evaluate(path, version="unknown")
            with path.open("a", encoding="utf-8") as stream:
                stream.write(path.read_text(encoding="utf-8").splitlines()[-1] + "\n")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                module.evaluate(path, version="v2")

    def test_partial_log_keeps_failures_and_truncated_text(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            run_pilot(ROOT / "experiments/pilot_config.json", directory,
                      generator_ids=["qwen3"], max_jobs=2)
            path = directory / "generations.jsonl"
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            results = [r for r in records if r["event"] == "result"]
            results[0].update(status="error", response=None,
                              error={"type": "TimeoutError", "code": None})
            results[1]["status"] = "non_stop"
            results[1]["response"].update(content="Duração: 60 minutos", finish_reason="length")
            path.write_text("".join(json.dumps(r) + "\n" for r in records))
            before = path.read_bytes()
            report = module.evaluate(path)
            self.assertTrue(report["simulated"])
            self.assertEqual(report["planned"], 27)
            self.assertEqual(report["completed"], 2)
            self.assertIsNone(report["records"][0]["metrics"])
            self.assertEqual(report["records"][0]["error"]["type"], "TimeoutError")
            self.assertEqual(report["records"][1]["operational"]["finish_reason"], "length")
            self.assertTrue(report["records"][1]["metrics"]["requirements"]["duration_minutes"]["detected_contradiction"])
            self.assertEqual(path.read_bytes(), before)
