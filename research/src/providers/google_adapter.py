"""Google GenAI adapter for the common Multi-LLM interface."""

from collections.abc import Mapping
from importlib.metadata import version
from time import perf_counter
from typing import Any

from models import GenerationRequest, Provider
from prompting import PromptArtifact
from providers.base import ProviderAdapter
from providers.common import require_config, require_content
from providers.models import ProviderResponse


class GoogleAdapter(ProviderAdapter):
    provider = Provider.GOOGLE

    @staticmethod
    def generation_parameters(request: GenerationRequest) -> dict[str, Any]:
        if request.model == "gemini-3.8-flash":
            return {
                "max_output_tokens": request.max_tokens,
                "thinking_config": {"thinking_level": "low"},
                "response_mime_type": "text/plain",
            }
        return {"temperature": request.temperature, "max_output_tokens": request.max_tokens}

    def generate(self, request: GenerationRequest, prompt: PromptArtifact,
                 connection_config: Mapping[str, Any]) -> ProviderResponse:
        from google import genai
        from google.genai import types

        api_key = require_config(connection_config, "api_key", "Google GenAI")
        parameters = self.generation_parameters(request)
        # Validate before constructing a client: unsupported SDKs must fail locally.
        config = types.GenerateContentConfig(**parameters)
        started = perf_counter()
        client_options = {}
        if connection_config.get("single_attempt"):
            client_options["http_options"] = types.HttpOptions(
                timeout=connection_config.get("timeout_ms", 60000),
                retry_options=types.HttpRetryOptions(attempts=1),
            )
        with genai.Client(api_key=api_key, **client_options) as client:
            response = client.models.generate_content(
                model=request.model,
                contents=prompt.text,
                config=config,
            )
        latency_ms = (perf_counter() - started) * 1000
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
        output_tokens = getattr(usage, "candidates_token_count", None) if usage else None
        candidates = getattr(response, "candidates", None) or []
        reason = getattr(candidates[0], "finish_reason", None) if candidates else None
        return ProviderResponse(
            content=require_content(response.text, "Google GenAI"),
            provider=self.provider,
            model=request.model,
            latency_ms=latency_ms,
            input_tokens=prompt_tokens,
            output_tokens=output_tokens,
            finish_reason=getattr(reason, "value", reason),
            provider_parameters=parameters,
            raw_metadata={
                "response_id": getattr(response, "response_id", None),
                "model_version": getattr(response, "model_version", None),
                "sdk_version": version("google-genai"),
                "thoughts_tokens": getattr(usage, "thoughts_token_count", None),
                "total_tokens": getattr(usage, "total_token_count", None),
                "cached_input_tokens": getattr(usage, "cached_content_token_count", None),
            },
        )
