"""Strict local parsing and validation of automatic judge responses."""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from pydantic import BaseModel, ConfigDict, Field

from experiment.judge_prompt import JUDGE_RESPONSE_SCHEMA_VERSION, JUDGE_RUBRIC_VERSION


JUDGE_RESPONSE_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "llm_judge_response.schema.json"
)


class JudgeResponseErrorCode(StrEnum):
    """Stable failure categories for computational reporting."""

    EMPTY_RESPONSE = "empty_response"
    INVALID_JSON = "invalid_json"
    DUPLICATE_KEY = "duplicate_key"
    NON_OBJECT_ROOT = "non_object_root"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    UNSUPPORTED_SCHEMA_VERSION = "unsupported_schema_version"
    UNSUPPORTED_RUBRIC_VERSION = "unsupported_rubric_version"
    INVALID_EVALUATION_ID = "invalid_evaluation_id"
    EVALUATION_ID_MISMATCH = "evaluation_id_mismatch"
    INVALID_SCORE = "invalid_score"
    INVALID_JUSTIFICATION = "invalid_justification"
    SCHEMA_VIOLATION = "schema_violation"


class JudgeResponseValidationError(ValueError):
    """Validation failure with a machine-readable category and JSON path."""

    def __init__(
        self,
        code: JudgeResponseErrorCode,
        message: str,
        json_path: str = "$",
    ) -> None:
        super().__init__(message)
        self.code = code
        self.json_path = json_path


class CriterionAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    score: int = Field(ge=1, le=4)
    justification: str = Field(min_length=1, max_length=1000)


class JudgeAssessments(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    semantic_fidelity: CriterionAssessment
    instructional_alignment: CriterionAssessment
    grade_appropriateness: CriterionAssessment
    coherence_feasibility: CriterionAssessment


class ValidatedJudgeResponse(BaseModel):
    """Typed representation produced only after JSON Schema validation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str
    rubric_version: str
    evaluation_id: str
    assessments: JudgeAssessments


class _DuplicateKeyError(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


@lru_cache(maxsize=1)
def _schema_validator() -> Draft202012Validator:
    schema = json.loads(JUDGE_RESPONSE_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _json_path(parts: list[Any]) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def _classify_schema_error(error: Any) -> JudgeResponseErrorCode:
    path = tuple(error.absolute_path)
    final_field = path[-1] if path else None

    if error.validator == "required":
        return JudgeResponseErrorCode.MISSING_REQUIRED_FIELD
    if error.validator == "additionalProperties":
        return JudgeResponseErrorCode.UNEXPECTED_FIELD
    if final_field == "schema_version" and error.validator == "const":
        return JudgeResponseErrorCode.UNSUPPORTED_SCHEMA_VERSION
    if final_field == "rubric_version" and error.validator == "const":
        return JudgeResponseErrorCode.UNSUPPORTED_RUBRIC_VERSION
    if final_field == "evaluation_id":
        return JudgeResponseErrorCode.INVALID_EVALUATION_ID
    if final_field == "score":
        return JudgeResponseErrorCode.INVALID_SCORE
    if final_field == "justification":
        return JudgeResponseErrorCode.INVALID_JUSTIFICATION
    return JudgeResponseErrorCode.SCHEMA_VIOLATION


def _enforce_strict_criterion_primitives(data: dict[str, Any]) -> None:
    """Reject JSON numbers such as 4.0 that JSON Schema treats as integers."""

    assessments = data.get("assessments")
    if not isinstance(assessments, dict):
        return
    for criterion, result in assessments.items():
        if not isinstance(result, dict):
            continue
        if "score" in result and type(result["score"]) is not int:
            raise JudgeResponseValidationError(
                JudgeResponseErrorCode.INVALID_SCORE,
                "The score must be encoded as a JSON integer without coercion",
                f"$.assessments.{criterion}.score",
            )
        if "justification" in result and not isinstance(result["justification"], str):
            raise JudgeResponseValidationError(
                JudgeResponseErrorCode.INVALID_JUSTIFICATION,
                "The justification must be a JSON string",
                f"$.assessments.{criterion}.justification",
            )


def parse_llm_judge_response(
    raw_response: str,
    expected_evaluation_id: str,
) -> ValidatedJudgeResponse:
    """Parse exactly one JSON object and validate it without repair or coercion."""

    if not isinstance(raw_response, str) or not raw_response.strip():
        raise JudgeResponseValidationError(
            JudgeResponseErrorCode.EMPTY_RESPONSE,
            "The judge response is empty",
        )

    try:
        data = json.loads(
            raw_response.strip(),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except _DuplicateKeyError as error:
        raise JudgeResponseValidationError(
            JudgeResponseErrorCode.DUPLICATE_KEY,
            f"Duplicate JSON key: {error}",
        ) from error
    except json.JSONDecodeError as error:
        raise JudgeResponseValidationError(
            JudgeResponseErrorCode.INVALID_JSON,
            f"Invalid JSON at line {error.lineno}, column {error.colno}",
        ) from error

    if not isinstance(data, dict):
        raise JudgeResponseValidationError(
            JudgeResponseErrorCode.NON_OBJECT_ROOT,
            "The judge response root must be a JSON object",
        )

    _enforce_strict_criterion_primitives(data)

    errors = sorted(
        _schema_validator().iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if errors:
        error = errors[0]
        raise JudgeResponseValidationError(
            _classify_schema_error(error),
            error.message,
            _json_path(list(error.absolute_path)),
        )

    if data["evaluation_id"] != expected_evaluation_id:
        raise JudgeResponseValidationError(
            JudgeResponseErrorCode.EVALUATION_ID_MISMATCH,
            "The response evaluation_id does not match the requested evaluation",
            "$.evaluation_id",
        )

    assert data["schema_version"] == JUDGE_RESPONSE_SCHEMA_VERSION
    assert data["rubric_version"] == JUDGE_RUBRIC_VERSION
    return ValidatedJudgeResponse.model_validate(data, strict=True)
