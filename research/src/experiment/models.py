"""Serializable record for one complete EduADocs generation."""

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ExecutionRecord(BaseModel):
    """Audit record containing no credentials or provider connection data."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "eduadocs-execution-v1.0.0"
    execution_id: str
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: Literal["success", "error"]
    request: dict[str, Any]
    prompt: dict[str, Any]
    provider_response: dict[str, Any]
    raw_response: str
    processed_response: str
    processing_warnings: list[str] = Field(default_factory=list)
    estimated_cost_usd: float | None = Field(default=None, ge=0)
    error: str | None = None
