"""Hugging Face Inference API adapter."""

from collections.abc import Mapping
from time import perf_counter
from typing import Any

import requests

from models import GenerationRequest, Provider
from prompting import PromptArtifact
from providers.base import ProviderAdapter
from providers.common import require_content
from providers.models import ProviderResponse


class HuggingFaceAdapter(ProviderAdapter):
    provider = Provider.HUGGINGFACE

    def generate(self, request: GenerationRequest, prompt: PromptArtifact,
                 connection_config: Mapping[str, Any]) -> ProviderResponse:
        if connection_config.get("use_local"):
            raise NotImplementedError(
                "Local Hugging Face execution remains in the legacy flow until a dedicated runtime adapter is added"
            )
        parameters = {
            "temperature": request.temperature,
            "max_new_tokens": request.max_tokens,
            "return_full_text": False,
        }
        headers = {"Content-Type": "application/json"}
        if connection_config.get("api_key"):
            headers["Authorization"] = f"Bearer {connection_config['api_key']}"
        started = perf_counter()
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{request.model}",
            headers=headers,
            json={"inputs": prompt.text, "parameters": parameters},
            timeout=connection_config.get("timeout", 60),
        )
        latency_ms = (perf_counter() - started) * 1000
        response.raise_for_status()
        data = response.json()
        item = data[0] if isinstance(data, list) and data else data
        content = item.get("generated_text") if isinstance(item, dict) else str(item)
        return ProviderResponse(
            content=require_content(content, "Hugging Face"),
            provider=self.provider,
            model=request.model,
            latency_ms=latency_ms,
            provider_parameters=parameters,
        )
