"""Outputs produced by the prompt-construction layer."""

from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True, slots=True)
class PromptArtifact:
    """Immutable and auditable prompt ready for an LLM provider."""

    text: str
    template_version: str
    expected_requirements: tuple[str, ...]
    semantic_payload_hash: str | None = None

    @property
    def sha256(self) -> str:
        """Stable identifier for the exact prompt text."""

        return sha256(self.text.encode("utf-8")).hexdigest()
