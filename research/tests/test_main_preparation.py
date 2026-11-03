"""Main catalog and common executor remain offline until the draft is closed."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_main_study import prepare
from experiment.pilot_runner import run_pilot


class MainPreparationTests(unittest.TestCase):
    def test_sol_metadata_does_not_misrepresent_omitted_temperature_as_zero(self):
        from experiment.judge_record import JudgeConfiguration
        config = json.loads((ROOT / "experiments/main_config.json").read_text(encoding="utf-8"))["judge"]["configuration"]
        parsed = JudgeConfiguration(**config)
        self.assertIsNone(parsed.temperature)
        self.assertIsNone(parsed.model_dump(mode="json")["temperature"])

    def test_complete_offline_plan_and_simulation(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            report = prepare(ROOT / "experiments/main_config.json", directory / "preparation")
            self.assertEqual(report["tasks"], 12)
            self.assertEqual(report["planned_generations"], 216)
            self.assertEqual(report["planned_judgments_if_all_valid"], 648)
            self.assertEqual(report["api_calls"], 0)
            self.assertEqual(len(report["literal_payload_checks"]), 12)
            for check in report["literal_payload_checks"]:
                self.assertEqual(len(check["states"]), 7)
            plan = json.loads((directory / "preparation/generation_plan.json").read_text(encoding="utf-8"))
            self.assertEqual(len({j["job_id"] for j in plan["jobs"]}), 216)
            for task in {j["task_id"] for j in plan["jobs"]}:
                selected = [j for j in plan["jobs"] if j["task_id"] == task and j["condition"] in ("c1", "c2")]
                self.assertEqual(len({j["payload_hash"] for j in selected}), 1)
            result = run_pilot(ROOT / "experiments/main_config.json", directory / "simulation")
            self.assertTrue(result["simulated"])
            self.assertEqual(result["completed"], 216)

    def test_live_draft_is_blocked_before_output_or_network(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "must-not-exist"
            config = json.loads((ROOT / "experiments/main_config.json").read_text(encoding="utf-8"))
            config["status"] = "draft_offline_only"
            draft = Path(temp) / "draft.json"
            draft.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "draft"):
                run_pilot(draft, path, simulated=False)
            self.assertFalse(path.exists())
