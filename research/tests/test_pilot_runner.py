"""Pilot scheduling, resume and failure preservation without APIs."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.pilot_runner import build_plan, run_pilot
from providers.models import ProviderResponse


class PilotRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "run"
        self.config_path = ROOT / "experiments/pilot_config.json"

    def test_plan_has_54_unique_jobs_and_shared_c1_c2_payload(self):
        config = json.loads(self.config_path.read_text(encoding="utf-8"))
        jobs = build_plan(config)
        self.assertEqual(jobs, build_plan(config))
        self.assertEqual(len({j["job_id"] for j in jobs}), 54)
        for gid in ("gemini", "qwen3"):
            self.assertEqual(sum(j["generator_id"] == gid for j in jobs), 27)
        for task in config["tasks"]:
            selected = [j for j in jobs if j["task_id"] == task["task_id"]]
            self.assertEqual(len(selected), 18)
            self.assertEqual(len({j["payload_hash"] for j in selected}), 1)

    def test_simulation_resume_does_not_rewrite_or_duplicate(self):
        first = run_pilot(self.config_path, self.output, max_jobs=5)
        self.assertEqual(first["completed"], 5)
        path = self.output / "generations.jsonl"
        prefix = path.read_bytes()
        resumed = run_pilot(self.config_path, self.output)
        self.assertEqual(resumed["completed"], 54)
        self.assertTrue(path.read_bytes().startswith(prefix))
        complete = path.read_bytes()
        run_pilot(self.config_path, self.output)
        self.assertEqual(path.read_bytes(), complete)

    def test_local_selection_never_calls_google_and_preserves_plan(self):
        config = json.loads(self.config_path.read_text(encoding="utf-8"))
        google = Mock()
        local = Mock()
        local.generate.return_value = ProviderResponse(
            provider="ollama", model=config["generators"]["qwen3"]["model"],
            content="Plano de teste", latency_ms=1, finish_reason="stop")
        report = run_pilot(self.config_path, self.output, simulated=False,
                           generator_ids=["qwen3"], adapters={"gemini": google, "qwen3": local})
        self.assertEqual(report["success"], 27)
        google.generate.assert_not_called()
        header = json.loads((self.output / "generations.jsonl").read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(header["config"], config)
        expected = json.loads(json.dumps([j for j in build_plan(config) if j["generator_id"] == "qwen3"]))
        self.assertEqual(header["jobs"], expected)
        with self.assertRaises(ValueError):
            run_pilot(self.config_path, self.output, generator_ids=["gemini"])

    def test_rejects_changed_configuration_before_call(self):
        run_pilot(self.config_path, self.output, max_jobs=1)
        config = json.loads(self.config_path.read_text(encoding="utf-8"))
        config["execution"]["shuffle_seed"] = 7
        changed = Path(self.temp.name) / "changed.json"
        changed.write_text(json.dumps(config))
        with self.assertRaises(ValueError):
            run_pilot(changed, self.output)
        with self.assertRaises(ValueError):
            run_pilot(self.config_path, self.output, simulated=False, adapters={"gemini": Mock(), "qwen3": Mock()})

    def test_failures_saved_and_not_automatically_retried(self):
        adapter = Mock()
        adapter.generate.side_effect = RuntimeError("secret must not enter log")
        adapters = {"gemini": adapter, "qwen3": adapter}
        run_pilot(self.config_path, self.output, simulated=False, adapters=adapters, max_jobs=1)
        adapter.generate.side_effect = None
        adapter.generate.return_value = ProviderResponse(
            provider="google", model="gemini-3.8-flash", content="Truncated content",
            latency_ms=1, finish_reason="MAX_TOKENS",
        )
        report = run_pilot(self.config_path, self.output, simulated=False,
                           adapters=adapters, max_jobs=1)
        self.assertEqual(adapter.generate.call_count, 2)
        self.assertEqual(report["failed_or_non_stop"], 2)
        log = (self.output / "generations.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("secret must not enter log", log)
        self.assertIn("Truncated content", log)

    def test_interruption_after_started_blocks_resume(self):
        adapter = Mock()
        adapter.generate.side_effect = KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            run_pilot(self.config_path, self.output, simulated=False, adapters={"gemini": adapter, "qwen3": adapter})
        with self.assertRaisesRegex(ValueError, "unresolved"):
            run_pilot(self.config_path, self.output, simulated=False, adapters={"gemini": adapter, "qwen3": adapter})
        self.assertEqual(adapter.generate.call_count, 1)
