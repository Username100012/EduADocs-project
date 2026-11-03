"""Local-only tests for strict parsing and classification of judge responses."""

import json
import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    JudgeResponseErrorCode,
    JudgeResponseValidationError,
    ValidatedJudgeResponse,
    parse_llm_judge_response,
)


EVALUATION_ID = "eval-7f3a91b4c6d84e20a5f813729b0c4d6e"
OTHER_EVALUATION_ID = "eval-8a4b02c5d7e94f31b6a924830c1d5e7f"


def valid_response() -> dict:
    return {
        "schema_version": "eduadocs-llm-judge-response-v1.0.0",
        "rubric_version": "eduadocs-llm-judge-v1.0.0",
        "evaluation_id": EVALUATION_ID,
        "assessments": {
            "semantic_fidelity": {"score": 3, "justification": "Atende ao tema."},
            "instructional_alignment": {
                "score": 2,
                "justification": "A avaliação está parcialmente alinhada.",
            },
            "grade_appropriateness": {
                "score": 4,
                "justification": "Linguagem compatível com o nível.",
            },
            "coherence_feasibility": {
                "score": 3,
                "justification": "A sequência é executável.",
            },
        },
    }


def parse(data: dict) -> ValidatedJudgeResponse:
    return parse_llm_judge_response(
        json.dumps(data, ensure_ascii=False),
        expected_evaluation_id=EVALUATION_ID,
    )


class LlmJudgeResponseParserTests(unittest.TestCase):
    def assert_error_code(self, code: JudgeResponseErrorCode, raw: str) -> None:
        with self.assertRaises(JudgeResponseValidationError) as context:
            parse_llm_judge_response(raw, EVALUATION_ID)
        self.assertEqual(context.exception.code, code)

    def test_parses_exact_valid_object_into_typed_model(self):
        result = parse(valid_response())
        self.assertIsInstance(result, ValidatedJudgeResponse)
        self.assertEqual(result.evaluation_id, EVALUATION_ID)
        self.assertEqual(result.assessments.semantic_fidelity.score, 3)

    def test_rejects_empty_invalid_json_and_non_object_root(self):
        self.assert_error_code(JudgeResponseErrorCode.EMPTY_RESPONSE, "   ")
        self.assert_error_code(JudgeResponseErrorCode.INVALID_JSON, "```json\n{}\n```")
        self.assert_error_code(JudgeResponseErrorCode.NON_OBJECT_ROOT, "[]")

    def test_rejects_duplicate_keys_without_silent_overwrite(self):
        raw = '{"schema_version":"a","schema_version":"b"}'
        self.assert_error_code(JudgeResponseErrorCode.DUPLICATE_KEY, raw)

    def test_classifies_missing_and_unexpected_fields(self):
        missing = valid_response()
        del missing["assessments"]["semantic_fidelity"]
        self.assert_error_code(
            JudgeResponseErrorCode.MISSING_REQUIRED_FIELD,
            json.dumps(missing),
        )

        unexpected = valid_response()
        unexpected["overall_score"] = 4
        self.assert_error_code(
            JudgeResponseErrorCode.UNEXPECTED_FIELD,
            json.dumps(unexpected),
        )

    def test_classifies_contract_version_errors(self):
        wrong_schema = valid_response()
        wrong_schema["schema_version"] = "future-schema"
        self.assert_error_code(
            JudgeResponseErrorCode.UNSUPPORTED_SCHEMA_VERSION,
            json.dumps(wrong_schema),
        )

        wrong_rubric = valid_response()
        wrong_rubric["rubric_version"] = "future-rubric"
        self.assert_error_code(
            JudgeResponseErrorCode.UNSUPPORTED_RUBRIC_VERSION,
            json.dumps(wrong_rubric),
        )

    def test_classifies_score_and_justification_errors(self):
        bad_score = valid_response()
        bad_score["assessments"]["semantic_fidelity"]["score"] = 4.0
        self.assert_error_code(
            JudgeResponseErrorCode.INVALID_SCORE,
            json.dumps(bad_score),
        )

        bad_justification = valid_response()
        bad_justification["assessments"]["semantic_fidelity"]["justification"] = ""
        self.assert_error_code(
            JudgeResponseErrorCode.INVALID_JUSTIFICATION,
            json.dumps(bad_justification),
        )

    def test_rejects_mismatched_evaluation_id(self):
        with self.assertRaises(JudgeResponseValidationError) as context:
            parse_llm_judge_response(
                json.dumps(valid_response()),
                expected_evaluation_id=OTHER_EVALUATION_ID,
            )
        self.assertEqual(
            context.exception.code,
            JudgeResponseErrorCode.EVALUATION_ID_MISMATCH,
        )
        self.assertEqual(context.exception.json_path, "$.evaluation_id")

    def test_does_not_coerce_string_score(self):
        response = valid_response()
        response["assessments"]["semantic_fidelity"]["score"] = "3"
        self.assert_error_code(
            JudgeResponseErrorCode.INVALID_SCORE,
            json.dumps(response),
        )


if __name__ == "__main__":
    unittest.main()
