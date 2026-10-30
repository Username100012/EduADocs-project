"""Normalized result returned by all provider adapters."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from models import Provider


class ProviderResponse(BaseModel):
    """Provider-neutral response and computational evaluation metadata."""

    model_config = ConfigDict(extra="forbid")

    content: str
    provider: Provider
    model: str
    latency_ms: float = Field(ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    finish_reason: str | None = None
    provider_parameters: dict[str, Any] = Field(default_factory=dict)
    raw_metadata: dict[str, Any] = Field(default_factory=dict)
