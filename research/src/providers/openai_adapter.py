"""OpenAI adapter for the common Multi-LLM interface."""

from collections.abc import Mapping
from time import perf_counter
from typing import Any

import requests

from models import GenerationRequest, Provider
from prompting import PromptArtifact
from providers.base import ProviderAdapter
from providers.common import require_config, require_content
from providers.models import ProviderResponse


class OpenAIAdapter(ProviderAdapter):
    provider = Provider.OPENAI

    def generate(self, request: GenerationRequest, prompt: PromptArtifact,
                 connection_config: Mapping[str, Any]) -> ProviderResponse:
        api_key = require_config(connection_config, "api_key", "OpenAI")
        parameters: dict[str, Any] = {"temperature": request.temperature}
        token_field = "max_completion_tokens" if request.model.startswith("gpt-5") else "max_tokens"
        parameters[token_field] = request.max_tokens
        payload = {
            "model": request.model,
            "messages": [{"role": "user", "content": prompt.text}],
            **parameters,
        }
        started = perf_counter()
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=connection_config.get("timeout", 60),
        )
        latency_ms = (perf_counter() - started) * 1000
        response.raise_for_status()
        data = response.json()
        choice = data["choices"][0]
        usage = data.get("usage") or {}
        return ProviderResponse(
            content=require_content(choice["message"]["content"], "OpenAI"),
            provider=self.provider,
            model=data.get("model", request.model),
            latency_ms=latency_ms,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
            finish_reason=choice.get("finish_reason"),
            provider_parameters=parameters,
            raw_metadata={"response_id": data.get("id"), "created": data.get("created")},
        )
