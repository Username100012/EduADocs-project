"""Verify local model identity and runtime parameters without invoking Ollama."""

import json
from pathlib import Path
import sys
from unittest.mock import Mock, patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.pilot_runner import build_plan, _request, verify_local_model, run_pilot
from providers.ollama_adapter import OllamaAdapter
from providers.models import ProviderResponse
from prompting import PromptArtifact
import tempfile


class OllamaPilotTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "experiments/pilot_config.json").read_text())
        self.local = self.config["generators"]["qwen3"]

    @patch("experiment.pilot_runner.requests.get")
    def test_digest_and_version_gate(self, get):
        tags, version = Mock(), Mock()
        tags.json.return_value = {"models": [{"name": self.local["model"],
                                             "digest": self.local["expected_digest"]}]}
        version.json.return_value = {"version": self.local["ollama_version"]}
        get.side_effect = [tags, version]
        self.assertEqual(verify_local_model(self.local)["verified_digest"], self.local["expected_digest"])
        tags.json.return_value["models"][0]["digest"] = "changed"
        get.side_effect = [tags]
        with self.assertRaises(ValueError):
            verify_local_model(self.local)

    @patch("providers.ollama_adapter.requests.post")
    def test_local_options_and_non_thinking_are_sent(self, post):
        job = next(j for j in build_plan(self.config) if j["generator_id"] == "qwen3")
        post.return_value.json.return_value = {
            "response": "Texto", "done_reason": "stop", "eval_count": 10,
            "model": self.local["model"], "eval_duration": 100,
        }
        response = OllamaAdapter().generate(
            _request(self.config, job), PromptArtifact(**job["prompt"]),
            {**self.local["generation_config"], "host": self.local["host"],
             "think": False, "keep_alive": "10m", "verified_digest": self.local["expected_digest"]},
        )
        body = post.call_args.kwargs["json"]
        self.assertFalse(body["think"])
        self.assertEqual(body["options"], self.local["generation_config"])
        self.assertEqual(response.raw_metadata["model_digest"], self.local["expected_digest"])

    def test_both_provider_adapters_route_correctly_and_resume_without_calls(self):
        adapters = {}
        for gid, g in self.config["generators"].items():
            adapter = Mock()
            adapter.generate.return_value = ProviderResponse(
                provider=g["provider"], model=g["model"], content="Simulated provider",
                finish_reason="STOP" if gid == "gemini" else "stop", latency_ms=1)
            adapters[gid] = adapter
        with tempfile.TemporaryDirectory() as directory:
            args = (ROOT / "experiments/pilot_config.json", Path(directory))
            report = run_pilot(*args, simulated=False, adapters=adapters)
            self.assertEqual(report["success"], 54)
            run_pilot(*args, simulated=False, adapters=adapters)
        for gid, adapter in adapters.items():
            self.assertEqual(adapter.generate.call_count, 27)
            for call in adapter.generate.call_args_list:
                self.assertEqual(call.args[0].model, self.config["generators"][gid]["model"])
