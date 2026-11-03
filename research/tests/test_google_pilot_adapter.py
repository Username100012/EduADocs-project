"""Google pilot parameters and response metadata without network access."""

import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from models import GenerationRequest, LessonPlanParameters
from prompting import PromptArtifact
from providers.google_adapter import GoogleAdapter


def request(model="gemini-3.8-flash"):
    return GenerationRequest(
        subject="Algoritmos", topic="Busca linear", grade_level="Superior",
        document_type="lesson_plan", provider="google", model=model,
        temperature=0.7, max_tokens=4096,
        pedagogical_parameters=LessonPlanParameters(),
    )


class GooglePilotAdapterTests(unittest.TestCase):
    def test_real_sdk_accepts_pilot_configuration_when_installed(self):
        try:
            from google.genai import types
        except ImportError:
            self.skipTest("google-genai is not installed in this interpreter")
        config = types.GenerateContentConfig(**GoogleAdapter.generation_parameters(request()))
        self.assertEqual(config.thinking_config.thinking_level.value, "LOW")

    def test_selected_parameters_match_single_pilot_configuration(self):
        config = json.loads((ROOT / "experiments/pilot_config.json").read_text())
        selected = config["generators"]["gemini"]
        parameters = GoogleAdapter.generation_parameters(request(selected["model"]))
        self.assertEqual(parameters, selected["generation_config"])
        self.assertFalse(set(parameters) & set(selected["omitted_parameters"]))

    def test_other_models_keep_existing_sampling_parameters(self):
        self.assertEqual(GoogleAdapter.generation_parameters(request("legacy-model")),
                         {"temperature": 0.7, "max_output_tokens": 4096})

    def test_adapter_passes_parameters_and_preserves_metadata(self):
        google, genai, types = (ModuleType(name) for name in
                                 ("google", "google.genai", "google.genai.types"))
        google.genai = genai
        genai.types = types
        types.GenerateContentConfig = MagicMock(side_effect=lambda **kwargs: kwargs)
        genai.Client = MagicMock()
        client = genai.Client.return_value.__enter__.return_value
        client.models.generate_content.return_value = SimpleNamespace(
            text="Plano gerado", response_id="response-test", model_version="returned-version",
            candidates=[SimpleNamespace(finish_reason=SimpleNamespace(value="STOP"))],
            usage_metadata=SimpleNamespace(prompt_token_count=100, candidates_token_count=200,
                                          thoughts_token_count=50, total_token_count=350,
                                          cached_content_token_count=0),
        )
        with patch.dict(sys.modules, {"google": google, "google.genai": genai,
                                      "google.genai.types": types}), patch(
            "providers.google_adapter.version", return_value="test-sdk"
        ):
            result = GoogleAdapter().generate(
                request(), PromptArtifact("Prompt", "v1", ()), {"api_key": "test-secret"}
            )
        self.assertEqual(result.finish_reason, "STOP")
        self.assertEqual(result.raw_metadata["model_version"], "returned-version")
        self.assertEqual(result.raw_metadata["thoughts_tokens"], 50)
        self.assertEqual(result.raw_metadata["sdk_version"], "test-sdk")
        self.assertNotIn("test-secret", result.model_dump_json())
        sent = client.models.generate_content.call_args.kwargs
        self.assertEqual(sent["config"], GoogleAdapter.generation_parameters(request()))
        genai.Client.return_value.__exit__.assert_called_once()
