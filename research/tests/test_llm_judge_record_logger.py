"""Tests for append-only persistence of auditable judge records."""

import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from filelock import FileLock
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    CandidateResponseSnapshot,
    JudgeAttemptError,
    JudgeConfiguration,
    JudgeExecutionRecord,
    JudgePromptSnapshot,
    JudgeRecordLogger,
    JudgeRecordPersistenceError,
    JudgeRecordPersistenceErrorCode,
    JudgeResponseErrorCode,
    LessonPlanSemanticPayload,
    build_llm_judge_prompt,
)


EVALUATION_ID = "eval-7f3a91b4c6d84e20a5f813729b0c4d6e"
CANDIDATE = "Plano candidato."


def build_record(record_id: str) -> JudgeExecutionRecord:
    payload = LessonPlanSemanticPayload(
        topic="Fotossíntese",
        grade_level="7º ano",
        learning_objectives="Explicar a fotossíntese",
        duration_minutes=50,
        methodology="Investigação",
        materials="Folhas e lanterna",
        assessment_strategy="Mapa conceitual",
    )
    prompt = build_llm_judge_prompt(EVALUATION_ID, payload, CANDIDATE)
    return JudgeExecutionRecord(
        record_id=record_id,
        evaluation_id=EVALUATION_ID,
        task_id="task-001",
        condition="c0",
        generation_execution_id="generation-001",
        repetition=1,
        status="error",
        prompt=JudgePromptSnapshot.from_artifact(prompt),
        candidate=CandidateResponseSnapshot.from_text(CANDIDATE),
        judge_configuration=JudgeConfiguration(
            provider="example-provider",
            model="judge-model",
            model_version="2026-01",
            temperature=0,
        ),
        raw_response="not-json",
        error=JudgeAttemptError(
            code=JudgeResponseErrorCode.INVALID_JSON,
            message="Invalid JSON",
            json_path="$",
        ),
    )


class LlmJudgeRecordLoggerTests(unittest.TestCase):
    def test_appends_one_json_object_per_line_without_rewriting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "judge_records.jsonl"
            logger = JudgeRecordLogger(path)
            first = build_record("record-001")
            second = build_record("record-002")

            logger.append(first)
            first_bytes = path.read_bytes()
            logger.append(second)
            final_bytes = path.read_bytes()

            self.assertTrue(final_bytes.startswith(first_bytes))
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["record_id"], "record-001")
            self.assertEqual(json.loads(lines[1])["record_id"], "record-002")
            # Windows may remove a released lock file. Check lock acquisition,
            # rather than its platform-dependent residue on disk.
            with patch("experiment.judge_record_logger.FileLock", wraps=FileLock) as factory:
                logger.append(build_record("record-003"))
                factory.assert_called_once_with(str(path) + ".lock")

    def test_rejects_duplicate_record_id_without_changing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "judge_records.jsonl"
            logger = JudgeRecordLogger(path)
            logger.append(build_record("record-001"))
            original = path.read_bytes()

            with self.assertRaises(JudgeRecordPersistenceError) as context:
                logger.append(build_record("record-001"))

            self.assertEqual(
                context.exception.code,
                JudgeRecordPersistenceErrorCode.DUPLICATE_RECORD_ID,
            )
            self.assertEqual(path.read_bytes(), original)

    def test_rejects_corrupt_existing_json_without_appending(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "judge_records.jsonl"
            path.write_text('{"record_id":', encoding="utf-8")
            original = path.read_bytes()

            with self.assertRaises(JudgeRecordPersistenceError) as context:
                JudgeRecordLogger(path).append(build_record("record-002"))

            self.assertEqual(
                context.exception.code,
                JudgeRecordPersistenceErrorCode.CORRUPT_LOG_LINE,
            )
            self.assertEqual(context.exception.line_number, 1)
            self.assertEqual(path.read_bytes(), original)

    def test_rejects_existing_object_without_record_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "judge_records.jsonl"
            path.write_text('{"schema_version":"unknown"}\n', encoding="utf-8")

            with self.assertRaises(JudgeRecordPersistenceError) as context:
                JudgeRecordLogger(path).append(build_record("record-002"))

            self.assertEqual(
                context.exception.code,
                JudgeRecordPersistenceErrorCode.MISSING_RECORD_ID,
            )

    def test_rejects_blank_line_in_existing_log(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "judge_records.jsonl"
            path.write_text("\n", encoding="utf-8")

            with self.assertRaises(JudgeRecordPersistenceError) as context:
                JudgeRecordLogger(path).append(build_record("record-002"))

            self.assertEqual(
                context.exception.code,
                JudgeRecordPersistenceErrorCode.CORRUPT_LOG_LINE,
            )


if __name__ == "__main__":
    unittest.main()
