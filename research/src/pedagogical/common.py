"""Shared conversion from the current form payload to canonical request fields."""

from collections.abc import Mapping
from typing import Any


def common_request_fields(form_data: Mapping[str, Any]) -> dict[str, Any]:
    llm_config = form_data.get("llm_config") or {}
    return {
        "subject": form_data.get("subject", ""),
        "topic": form_data.get("topic", ""),
        "grade_level": form_data.get("grade_level", ""),
        "language": form_data.get("language") or "pt-BR",
        "provider": llm_config.get("provider"),
        "model": llm_config.get("model", ""),
        "temperature": llm_config.get("temperature", 0.7),
        "max_tokens": llm_config.get("max_tokens", 2000),
    }
