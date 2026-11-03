"""Shared helpers for provider adapters."""

from collections.abc import Mapping
from typing import Any


def require_config(config: Mapping[str, Any], name: str, provider: str) -> Any:
    value = config.get(name)
    if value is None or value == "":
        raise ValueError(f"{name} is required for the {provider} provider")
    return value


def require_content(content: object, provider: str) -> str:
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"{provider} returned an empty response")
    return content
