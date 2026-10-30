"""Registry and entry point for the Multi-LLM provider adapters."""

from collections.abc import Mapping
from typing import Any

from models import GenerationRequest, Provider
from prompting import PromptArtifact
from providers.base import ProviderAdapter
from providers.google_adapter import GoogleAdapter
from providers.huggingface_adapter import HuggingFaceAdapter
from providers.models import ProviderResponse
from providers.ollama_adapter import OllamaAdapter
from providers.openai_adapter import OpenAIAdapter


class ProviderGateway:
    """Select one adapter while keeping callers independent of provider APIs."""

    def __init__(self, adapters: list[ProviderAdapter] | None = None) -> None:
        available = (
            [OpenAIAdapter(), GoogleAdapter(), HuggingFaceAdapter(), OllamaAdapter()]
            if adapters is None
            else adapters
        )
        self._adapters = {adapter.provider: adapter for adapter in available}

    def generate(
        self,
        request: GenerationRequest,
        prompt: PromptArtifact,
        connection_config: Mapping[str, Any],
    ) -> ProviderResponse:
        try:
            adapter = self._adapters[request.provider]
        except KeyError as error:
            raise ValueError(f"No adapter registered for provider: {request.provider.value}") from error
        return adapter.generate(request, prompt, connection_config)
