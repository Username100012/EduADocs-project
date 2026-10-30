"""Normalize generated text while preserving the raw provider response."""

import re

from pydantic import BaseModel, ConfigDict, Field


class ProcessedResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_content: str
    content: str
    warnings: list[str] = Field(default_factory=list)


def process_response(raw_content: str) -> ProcessedResponse:
    """Apply provider-neutral cleanup without changing pedagogical meaning."""

    if not raw_content or not raw_content.strip():
        raise ValueError("The model returned an empty response")

    warnings: list[str] = []
    content, removed_blocks = re.subn(
        r"<think>.*?</think>", "", raw_content, flags=re.IGNORECASE | re.DOTALL
    )
    content = re.sub(r"<think\s*/>", "", content, flags=re.IGNORECASE)
    if removed_blocks:
        warnings.append("reasoning_blocks_removed")

    content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content).strip()
    if not content:
        raise ValueError("The response became empty after processing")

    return ProcessedResponse(raw_content=raw_content, content=content, warnings=warnings)
