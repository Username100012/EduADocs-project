"""Frozen execution manifest for the automatic LLM judge."""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from experiment.judge_record import JudgeConfiguration
from experiment.judge_response import JudgeResponseErrorCode


JUDGE_MANIFEST_SCHEMA_VERSION = "eduadocs-judge-manifest-v1.0.0"
REQUIRED_ARTIFACTS = (
    "computational_rubric",
    "judge_model_selection",
    "judge_rubric",
    "judge_response_schema",
    "judge_prompt_source",
    "judge_protocol",
)


class ManifestModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ArtifactFingerprint(ManifestModel):
    artifact_id: str = Field(min_length=1)
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class JudgeAttemptPolicy(ManifestModel):
    max_attempts_per_repetition: Literal[2] = 2
    preserve_every_attempt: Literal[True] = True
    replace_failed_repetition: Literal[False] = False
    retry_validation_errors_once: tuple[JudgeResponseErrorCode, ...] = tuple(
        JudgeResponseErrorCode
    )

    @model_validator(mode="after")
    def require_unique_complete_error_policy(self) -> "JudgeAttemptPolicy":
        configured = tuple(self.retry_validation_errors_once)
        if len(configured) != len(set(configured)):
            raise ValueError("retry validation error codes must be unique")
        if set(configured) != set(JudgeResponseErrorCode):
            raise ValueError("retry policy must explicitly cover every validation error")
        return self


class JudgeBlindingPolicy(ManifestModel):
    hide_condition: Literal[True] = True
    hide_generator_model: Literal[True] = True
    hide_provider: Literal[True] = True
    opaque_evaluation_id: Literal[True] = True
    pointwise_evaluation: Literal[True] = True


class JudgeExecutionManifest(ManifestModel):
    """Immutable configuration that identifies one reproducible judge run."""

    schema_version: Literal["eduadocs-judge-manifest-v1.0.0"] = (
        JUDGE_MANIFEST_SCHEMA_VERSION
    )
    manifest_id: str = Field(pattern=r"^judge-manifest-[a-z0-9._-]+$")
    status: Literal["frozen"] = "frozen"
    frozen_at: datetime
    judge_configuration: JudgeConfiguration
    repetitions_per_response: Literal[3] = 3
    attempt_policy: JudgeAttemptPolicy = Field(default_factory=JudgeAttemptPolicy)
    blinding_policy: JudgeBlindingPolicy = Field(default_factory=JudgeBlindingPolicy)
    artifacts: tuple[ArtifactFingerprint, ...]

    @model_validator(mode="after")
    def require_exact_artifact_set(self) -> "JudgeExecutionManifest":
        artifact_ids = [artifact.artifact_id for artifact in self.artifacts]
        if len(artifact_ids) != len(set(artifact_ids)):
            raise ValueError("artifact_id values must be unique")
        if set(artifact_ids) != set(REQUIRED_ARTIFACTS):
            raise ValueError("manifest must contain exactly the required artifacts")
        return self

    def canonical_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    @property
    def manifest_hash(self) -> str:
        return sha256(self.canonical_json().encode("utf-8")).hexdigest()

    def save_frozen(self, path: Path | str) -> None:
        """Create a manifest once; refusing overwrite preserves the frozen state."""

        manifest_path = Path(path)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(
                json.dumps(
                    self.model_dump(mode="json"),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )


def fingerprint_artifact(
    workspace_root: Path | str,
    artifact_id: str,
    relative_path: str,
) -> ArtifactFingerprint:
    """Hash one regular file inside the workspace using its exact bytes."""

    root = Path(workspace_root).resolve()
    pure_relative = PurePosixPath(relative_path)
    if pure_relative.is_absolute() or ".." in pure_relative.parts:
        raise ValueError("artifact path must be a safe workspace-relative path")
    artifact_path = (root / Path(*pure_relative.parts)).resolve()
    if root not in artifact_path.parents or not artifact_path.is_file():
        raise ValueError("artifact must be a regular file inside the workspace")
    return ArtifactFingerprint(
        artifact_id=artifact_id,
        path=pure_relative.as_posix(),
        sha256=sha256(artifact_path.read_bytes()).hexdigest(),
    )


def fingerprint_required_judge_artifacts(
    workspace_root: Path | str,
) -> tuple[ArtifactFingerprint, ...]:
    paths = {
        "computational_rubric": "experiments/computational_rubric.v1.json",
        "judge_model_selection": "experiments/judge_model_selection.v1.json",
        "judge_rubric": "experiments/llm_judge_rubric.v1.json",
        "judge_response_schema": "experiments/llm_judge_response.schema.json",
        "judge_prompt_source": "src/experiment/judge_prompt.py",
        "judge_protocol": "docs/LLM_AS_JUDGE_PROTOCOL.md",
    }
    return tuple(
        fingerprint_artifact(workspace_root, artifact_id, relative_path)
        for artifact_id, relative_path in paths.items()
    )
