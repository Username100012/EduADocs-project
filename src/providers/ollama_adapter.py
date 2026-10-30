"""Ollama adapter for locally executed models."""

from collections.abc import Mapping
from time import perf_counter
from typing import Any

import requests

from models import GenerationRequest, Provider
from prompting import PromptArtifact
from providers.base import ProviderAdapter
from providers.common import require_config, require_content
from providers.models import ProviderResponse


class OllamaAdapter(ProviderAdapter):
    provider = Provider.OLLAMA

    @staticmethod
    def generation_parameters(request, connection_config):
        parameters = {"temperature": request.temperature, "num_predict": request.max_tokens}
        for name in ("seed", "num_ctx"):
            if name in connection_config:
                parameters[name] = connection_config[name]
        return parameters

    def generate(self, request: GenerationRequest, prompt: PromptArtifact,
                 connection_config: Mapping[str, Any]) -> ProviderResponse:
        host = str(require_config(connection_config, "host", "Ollama")).rstrip("/")
        parameters = self.generation_parameters(request, connection_config)
        payload = {"model": request.model, "prompt": prompt.text,
                   "stream": False, "options": parameters}
        for name in ("think", "keep_alive"):
            if name in connection_config:
                payload[name] = connection_config[name]
        started = perf_counter()
        response = requests.post(
            f"{host}/api/generate",
            json=payload,
            timeout=connection_config.get("timeout", 300),
        )
        latency_ms = (perf_counter() - started) * 1000
        response.raise_for_status()
        data = response.json()
        return ProviderResponse(
            content=require_content(data.get("response"), "Ollama"),
            provider=self.provider,
            model=data.get("model", request.model),
            latency_ms=latency_ms,
            input_tokens=data.get("prompt_eval_count"),
            output_tokens=data.get("eval_count"),
            finish_reason=data.get("done_reason"),
            provider_parameters={**parameters, **{
                k: payload[k] for k in ("think", "keep_alive") if k in payload
            }},
            raw_metadata={
                "total_duration_ns": data.get("total_duration"),
                "load_duration_ns": data.get("load_duration"),
                "eval_duration_ns": data.get("eval_duration"),
                "prompt_eval_duration_ns": data.get("prompt_eval_duration"),
                "model_digest": connection_config.get("verified_digest"),
                "ollama_version": connection_config.get("verified_version"),
            },
        )
