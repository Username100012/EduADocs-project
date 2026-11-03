"""Contract implemented by every LLM provider adapter."""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from models import GenerationRequest, Provider
from prompting import PromptArtifact
from providers.models import ProviderResponse


class ProviderAdapter(ABC):
    """Translate a canonical request into one provider-specific API call."""

    provider: Provider

    @abstractmethod
    def generate(
        self,
        request: GenerationRequest,
        prompt: PromptArtifact,
        connection_config: Mapping[str, Any],
    ) -> ProviderResponse:
        """Execute one generation without persisting credentials."""
