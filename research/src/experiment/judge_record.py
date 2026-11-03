"""Auditable records for LLM-judge attempts, without provider execution logic."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from experiment.judge_response import (
    JudgeResponseErrorCode,
    JudgeResponseValidationError,
    ValidatedJudgeResponse,
)
from prompting import PromptArtifact


JUDGE_RECORD_SCHEMA_VERSION = "eduadocs-judge-record-v1.0.0"
_FORBIDDEN_CREDENTIAL_KEYS = {
    "api_key",
    "apikey",
    "authorization",
    "password",
    "secret",
    "token",
}


def _text_sha256(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _contains_credential_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            normalized_key = str(key).lower().replace("-", "_")
            if normalized_key in _FORBIDDEN_CREDENTIAL_KEYS:
                return True
            if _contains_credential_key(nested_value):
                return True
    elif isinstance(value, (list, tuple)):
        return any(_contains_credential_key(item) for item in value)
    return False


class JudgePromptSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    text: str = Field(min_length=1)
    template_version: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    semantic_payload_hash: str = Field(pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def verify_hash(self) -> "JudgePromptSnapshot":
        if self.sha256 != _text_sha256(self.text):
            raise ValueError("prompt sha256 does not match prompt text")
        return self

    @classmethod
    def from_artifact(cls, artifact: PromptArtifact) -> "JudgePromptSnapshot":
        if artifact.semantic_payload_hash is None:
            raise ValueError("judge prompt must identify its semantic payload")
        return cls(
            text=artifact.text,
            template_version=artifact.template_version,
            sha256=artifact.sha256,
            semantic_payload_hash=artifact.semantic_payload_hash,
        )


class CandidateResponseSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    text: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def verify_hash(self) -> "CandidateResponseSnapshot":
        if self.sha256 != _text_sha256(self.text):
            raise ValueError("candidate sha256 does not match candidate text")
        return self

    @classmethod
    def from_text(cls, text: str) -> "CandidateResponseSnapshot":
        if not text:
            raise ValueError("candidate response must be non-empty")
        return cls(text=text, sha256=_text_sha256(text))


class JudgeConfiguration(BaseModel):
    """Reproducibility metadata; credentials are explicitly forbidden."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    # Required field: None explicitly means omitted on the wire, not zero.
    temperature: float | None = Field(ge=0)
    seed: int | None = None
    max_output_tokens: int | None = Field(default=None, ge=1)
    response_format: Literal["json_schema"] = "json_schema"
    provider_parameters: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def reject_credentials(self) -> "JudgeConfiguration":
        if _contains_credential_key(self.provider_parameters):
            raise ValueError("provider_parameters must not contain credentials")
        return self


class JudgeRuntimeMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    latency_ms: float | None = Field(default=None, ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    finish_reason: str | None = None
    raw_metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def reject_credentials(self) -> "JudgeRuntimeMetadata":
        if _contains_credential_key(self.raw_metadata):
            raise ValueError("raw_metadata must not contain credentials")
        return self


class JudgeAttemptError(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    code: JudgeResponseErrorCode
    message: str = Field(min_length=1)
    json_path: str = Field(min_length=1)

    @classmethod
    def from_validation_error(
        cls, error: JudgeResponseValidationError
    ) -> "JudgeAttemptError":
        return cls(code=error.code, message=str(error), json_path=error.json_path)


class JudgeExecutionRecord(BaseModel):
    """One immutable and self-checking judgment attempt."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["eduadocs-judge-record-v1.0.0"] = (
        JUDGE_RECORD_SCHEMA_VERSION
    )
    record_id: str = Field(min_length=1)
    evaluation_id: str = Field(
        pattern=r"^eval-[a-f0-9]{32}$"
    )
    task_id: str = Field(min_length=1)
    condition: Literal["c0", "c1", "c2"]
    generation_execution_id: str = Field(min_length=1)
    repetition: int = Field(ge=1)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: Literal["success", "error"]
    prompt: JudgePromptSnapshot
    candidate: CandidateResponseSnapshot
    judge_configuration: JudgeConfiguration
    runtime: JudgeRuntimeMetadata = Field(default_factory=JudgeRuntimeMetadata)
    raw_response: str
    validated_response: ValidatedJudgeResponse | None = None
    error: JudgeAttemptError | None = None

    @model_validator(mode="after")
    def enforce_status_invariants(self) -> "JudgeExecutionRecord":
        if self.status == "success":
            if self.validated_response is None or self.error is not None:
                raise ValueError(
                    "successful record requires validated_response and forbids error"
                )
            if self.validated_response.evaluation_id != self.evaluation_id:
                raise ValueError("validated response evaluation_id does not match record")
        else:
            if self.error is None or self.validated_response is not None:
                raise ValueError(
                    "error record requires error and forbids validated_response"
                )
        return self
