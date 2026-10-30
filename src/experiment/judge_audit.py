"""Offline integration of frozen manifests, parser and append-only records."""

import json
import os
from pathlib import Path
from typing import Literal

from filelock import FileLock
from pydantic import BaseModel, ConfigDict, Field

from experiment.judge_manifest import (
    JudgeExecutionManifest, fingerprint_required_judge_artifacts,
)
from experiment.judge_prompt import build_llm_judge_prompt
from experiment.judge_record import (
    CandidateResponseSnapshot, JudgeAttemptError, JudgeExecutionRecord,
    JudgePromptSnapshot,
)
from experiment.judge_response import (
    JudgeResponseValidationError, parse_llm_judge_response,
)
from experiment.semantic_payload import LessonPlanSemanticPayload


class AuditedJudgeAttempt(BaseModel):
    """Envelope linking each existing record to a manifest and an attempt."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    schema_version: Literal["eduadocs-audited-judge-attempt-v1.0.0"] = (
        "eduadocs-audited-judge-attempt-v1.0.0"
    )
    manifest_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    attempt: int = Field(ge=1, le=2)
    record: JudgeExecutionRecord


class OfflineJudgeAudit:
    """Validate simulated attempts; never invokes a model or provider."""

    def __init__(self, workspace_root: Path, manifest_path: Path, log_path: Path):
        self.root = workspace_root
        self.manifest_path = manifest_path
        self.log_path = log_path
        self.manifest = self.verify_manifest()

    def verify_manifest(self) -> JudgeExecutionManifest:
        manifest = JudgeExecutionManifest.model_validate_json(
            self.manifest_path.read_text(encoding="utf-8"), strict=True
        )
        seal_path = self.manifest_path.with_suffix(".canonical.sha256")
        if manifest.manifest_hash != seal_path.read_text(encoding="utf-8").split()[0]:
            raise ValueError("manifest seal mismatch")
        current = fingerprint_required_judge_artifacts(self.root)
        if manifest.artifacts != current:
            raise ValueError("frozen artifact mismatch")
        selection = next(a for a in current if a.artifact_id == "judge_model_selection")
        config = json.loads((self.root / selection.path).read_text(encoding="utf-8"))
        if manifest.judge_configuration.model_dump(mode="json") != config["judge_configuration"]:
            raise ValueError("selected configuration differs from manifest")
        return manifest

    def capture(
        self, *, evaluation_id: str, payload: LessonPlanSemanticPayload,
        candidate: str, raw_response: str, task_id: str, condition: str,
        generation_execution_id: str, repetition: int, attempt: int,
    ) -> AuditedJudgeAttempt:
        """Build a record by parsing the supplied raw response locally."""
        self.verify_manifest()
        if not 1 <= repetition <= self.manifest.repetitions_per_response:
            raise ValueError("repetition outside frozen policy")
        prompt = build_llm_judge_prompt(evaluation_id, payload, candidate)
        result, error = None, None
        try:
            result = parse_llm_judge_response(raw_response, evaluation_id)
        except JudgeResponseValidationError as failure:
            error = JudgeAttemptError.from_validation_error(failure)
        record = JudgeExecutionRecord(
            record_id=f"{evaluation_id}-r{repetition}-a{attempt}",
            evaluation_id=evaluation_id, task_id=task_id, condition=condition,
            generation_execution_id=generation_execution_id, repetition=repetition,
            status="error" if error else "success",
            prompt=JudgePromptSnapshot.from_artifact(prompt),
            candidate=CandidateResponseSnapshot.from_text(candidate),
            judge_configuration=self.manifest.judge_configuration,
            raw_response=raw_response, validated_response=result, error=error,
        )
        return AuditedJudgeAttempt(
            manifest_hash=self.manifest.manifest_hash, attempt=attempt, record=record
        )

    def append(self, entry: AuditedJudgeAttempt, payload: LessonPlanSemanticPayload) -> None:
        """Revalidate evidence and history under one lock before appending."""
        self.verify_manifest()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with FileLock(str(self.log_path) + ".lock"):
            entries = []
            if self.log_path.exists():
                raw_log = self.log_path.read_text(encoding="utf-8")
                if raw_log and not raw_log.endswith("\n"):
                    raise ValueError("incomplete JSONL tail")
                entries = [
                    AuditedJudgeAttempt.model_validate_json(line)
                    for line in raw_log.splitlines()
                ]
            record = entry.record
            rebuilt = self.capture(
                evaluation_id=record.evaluation_id, payload=payload,
                candidate=record.candidate.text, raw_response=record.raw_response,
                task_id=record.task_id, condition=record.condition,
                generation_execution_id=record.generation_execution_id,
                repetition=record.repetition, attempt=entry.attempt,
            )
            expected = rebuilt.record.model_dump(exclude={"completed_at"})
            actual = record.model_dump(exclude={"completed_at"})
            if entry.manifest_hash != self.manifest.manifest_hash or actual != expected:
                raise ValueError("attempt evidence differs from reconstructed record")
            for prior in entries:
                if prior.manifest_hash != entry.manifest_hash:
                    raise ValueError("mixed manifests in audit log")
                if prior.record.record_id == record.record_id:
                    raise ValueError("duplicate record_id")
            history = [e for e in entries if e.record.evaluation_id == record.evaluation_id]
            if entry.attempt != len(history) + 1:
                raise ValueError("invalid attempt sequence")
            if history:
                previous = history[-1].record
                if previous.status != "error" or previous.error.code not in (
                    self.manifest.attempt_policy.retry_validation_errors_once
                ):
                    raise ValueError("retry after success or ineligible failure")
                for field in (
                    "prompt", "candidate", "task_id", "condition", "repetition",
                    "generation_execution_id", "judge_configuration",
                ):
                    if getattr(previous, field) != getattr(record, field):
                        raise ValueError("retry changed judgment inputs")
            with self.log_path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(entry.model_dump_json() + "\n")
                stream.flush()
                os.fsync(stream.fileno())
