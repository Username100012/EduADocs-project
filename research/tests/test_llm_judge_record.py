"""Tests for immutable and auditable LLM-judge attempt records."""

import json
import sys
import unittest
from pathlib import Path

from pydantic import ValidationError


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    CandidateResponseSnapshot,
    JudgeAttemptError,
    JudgeConfiguration,
    JudgeExecutionRecord,
    JudgePromptSnapshot,
    JudgeResponseValidationError,
    LessonPlanSemanticPayload,
    build_llm_judge_prompt,
    parse_llm_judge_response,
)


EVALUATION_ID = "eval-7f3a91b4c6d84e20a5f813729b0c4d6e"
OTHER_EVALUATION_ID = "eval-8a4b02c5d7e94f31b6a924830c1d5e7f"
CANDIDATE = "Plano candidato sobre fotossíntese."


def payload() -> LessonPlanSemanticPayload:
    return LessonPlanSemanticPayload(
        topic="Fotossíntese",
        grade_level="7º ano",
        learning_objectives="Explicar as etapas da fotossíntese",
        duration_minutes=50,
        methodology="Investigação",
        materials="Folhas e lanterna",
        assessment_strategy="Mapa conceitual",
    )


def valid_raw_response() -> str:
    data = {
        "schema_version": "eduadocs-llm-judge-response-v1.0.0",
        "rubric_version": "eduadocs-llm-judge-v1.0.0",
        "evaluation_id": EVALUATION_ID,
        "assessments": {
            name: {"score": 3, "justification": "Há evidência textual."}
            for name in (
                "semantic_fidelity",
                "instructional_alignment",
                "grade_appropriateness",
                "coherence_feasibility",
            )
        },
    }
    return json.dumps(data, ensure_ascii=False)


def common_fields() -> dict:
    artifact = build_llm_judge_prompt(EVALUATION_ID, payload(), CANDIDATE)
    return {
        "record_id": "judge-record-001",
        "evaluation_id": EVALUATION_ID,
        "task_id": "task-001",
        "condition": "c0",
        "generation_execution_id": "generation-001",
        "repetition": 1,
        "prompt": JudgePromptSnapshot.from_artifact(artifact),
        "candidate": CandidateResponseSnapshot.from_text(CANDIDATE),
        "judge_configuration": JudgeConfiguration(
            provider="example-provider",
            model="judge-model",
            model_version="2026-01",
            temperature=0,
            seed=42,
            max_output_tokens=1000,
        ),
    }


class LlmJudgeRecordTests(unittest.TestCase):
    def test_builds_serializable_success_record(self):
        raw = valid_raw_response()
        record = JudgeExecutionRecord(
            **common_fields(),
            status="success",
            raw_response=raw,
            validated_response=parse_llm_judge_response(raw, EVALUATION_ID),
        )

        serialized = json.loads(record.model_dump_json())
        self.assertEqual(serialized["schema_version"], "eduadocs-judge-record-v1.0.0")
        self.assertEqual(serialized["condition"], "c0")
        self.assertEqual(len(serialized["prompt"]["sha256"]), 64)
        self.assertEqual(len(serialized["candidate"]["sha256"]), 64)
        self.assertIsNone(serialized["error"])

    def test_builds_error_record_from_classified_parser_error(self):
        with self.assertRaises(JudgeResponseValidationError) as context:
            parse_llm_judge_response("not-json", EVALUATION_ID)

        record = JudgeExecutionRecord(
            **common_fields(),
            status="error",
            raw_response="not-json",
            error=JudgeAttemptError.from_validation_error(context.exception),
        )
        self.assertEqual(record.error.code, "invalid_json")
        self.assertIsNone(record.validated_response)

    def test_enforces_mutually_exclusive_success_and_error_states(self):
        with self.assertRaises(ValidationError):
            JudgeExecutionRecord(
                **common_fields(),
                status="success",
                raw_response="{}",
            )
        with self.assertRaises(ValidationError):
            JudgeExecutionRecord(
                **common_fields(),
                status="error",
                raw_response="{}",
            )

    def test_rejects_tampered_prompt_and_candidate_hashes(self):
        artifact = build_llm_judge_prompt(EVALUATION_ID, payload(), CANDIDATE)
        with self.assertRaises(ValidationError):
            JudgePromptSnapshot(
                text=artifact.text,
                template_version=artifact.template_version,
                sha256="0" * 64,
                semantic_payload_hash=artifact.semantic_payload_hash,
            )
        with self.assertRaises(ValidationError):
            CandidateResponseSnapshot(text=CANDIDATE, sha256="0" * 64)

    def test_rejects_credentials_in_nested_configuration(self):
        with self.assertRaises(ValidationError):
            JudgeConfiguration(
                provider="provider",
                model="model",
                model_version="version",
                temperature=0,
                provider_parameters={"headers": {"Authorization": "secret"}},
            )

    def test_rejects_response_for_another_evaluation(self):
        raw = valid_raw_response()
        validated = parse_llm_judge_response(raw, EVALUATION_ID)
        fields = common_fields()
        fields["evaluation_id"] = OTHER_EVALUATION_ID
        with self.assertRaises(ValidationError):
            JudgeExecutionRecord(
                **fields,
                status="success",
                raw_response=raw,
                validated_response=validated,
            )


if __name__ == "__main__":
    unittest.main()
