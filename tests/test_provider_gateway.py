"""Contract tests for the provider-independent gateway."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from models import Provider  # noqa: E402
from pedagogical import lesson_plan_request_from_form  # noqa: E402
from prompting import build_lesson_plan_prompt  # noqa: E402
from providers import ProviderGateway, ProviderResponse  # noqa: E402
from providers.base import ProviderAdapter  # noqa: E402


class FakeGoogleAdapter(ProviderAdapter):
    provider = Provider.GOOGLE

    def generate(self, request, prompt, connection_config):
        self.received_key = connection_config.get("api_key")
        return ProviderResponse(
            content="# Plano de aula",
            provider=self.provider,
            model=request.model,
            latency_ms=12.5,
            input_tokens=100,
            output_tokens=200,
            provider_parameters={"temperature": request.temperature},
        )


class ProviderGatewayTests(unittest.TestCase):
    def setUp(self):
        self.request = lesson_plan_request_from_form({
            "subject": "Ciências",
            "topic": "Água",
            "grade_level": "6º ano",
            "language": "pt-BR",
            "duration_minutes": 50,
            "llm_config": {"provider": "google", "model": "test-model"},
        })
        self.prompt = build_lesson_plan_prompt(self.request)

    def test_gateway_selects_adapter_and_normalizes_response(self):
        adapter = FakeGoogleAdapter()
        response = ProviderGateway([adapter]).generate(
            self.request, self.prompt, {"api_key": "temporary-secret"}
        )
        self.assertEqual(response.content, "# Plano de aula")
        self.assertEqual(response.input_tokens, 100)
        self.assertEqual(adapter.received_key, "temporary-secret")
        self.assertNotIn("temporary-secret", response.model_dump_json())

    def test_unregistered_provider_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "No adapter registered"):
            ProviderGateway([]).generate(self.request, self.prompt, {})


if __name__ == "__main__":
    unittest.main()
