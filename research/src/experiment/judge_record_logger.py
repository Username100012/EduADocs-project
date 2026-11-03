"""Append-only JSONL persistence for auditable LLM-judge records."""

from __future__ import annotations

from enum import StrEnum
import json
import os
from pathlib import Path
from typing import Any

from filelock import FileLock

from experiment.judge_record import JudgeExecutionRecord


DEFAULT_JUDGE_LOG_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "judge_records.jsonl"
)


class JudgeRecordPersistenceErrorCode(StrEnum):
    DUPLICATE_RECORD_ID = "duplicate_record_id"
    CORRUPT_LOG_LINE = "corrupt_log_line"
    MISSING_RECORD_ID = "missing_record_id"


class JudgeRecordPersistenceError(RuntimeError):
    """Persistence failure with a stable category and optional line number."""

    def __init__(
        self,
        code: JudgeRecordPersistenceErrorCode,
        message: str,
        line_number: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.line_number = line_number


def _read_record_id(line: str, line_number: int) -> str:
    try:
        data: Any = json.loads(line)
    except json.JSONDecodeError as error:
        raise JudgeRecordPersistenceError(
            JudgeRecordPersistenceErrorCode.CORRUPT_LOG_LINE,
            f"Invalid JSON in judge record log at line {line_number}",
            line_number,
        ) from error

    if not isinstance(data, dict):
        raise JudgeRecordPersistenceError(
            JudgeRecordPersistenceErrorCode.CORRUPT_LOG_LINE,
            f"Judge record log line {line_number} is not a JSON object",
            line_number,
        )

    record_id = data.get("record_id")
    if not isinstance(record_id, str) or not record_id:
        raise JudgeRecordPersistenceError(
            JudgeRecordPersistenceErrorCode.MISSING_RECORD_ID,
            f"Judge record log line {line_number} has no valid record_id",
            line_number,
        )
    return record_id


class JudgeRecordLogger:
    """Persist immutable records without rewriting or silently skipping data."""

    def __init__(self, path: Path | str = DEFAULT_JUDGE_LOG_PATH) -> None:
        self.path = Path(path)
        self.lock_path = Path(str(self.path) + ".lock")

    def append(self, record: JudgeExecutionRecord) -> None:
        """Atomically check uniqueness and append one UTF-8 JSON object."""

        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock = FileLock(str(self.lock_path))
        with lock:
            if self.path.exists():
                with self.path.open("r", encoding="utf-8") as stream:
                    for line_number, line in enumerate(stream, start=1):
                        if not line.strip():
                            raise JudgeRecordPersistenceError(
                                JudgeRecordPersistenceErrorCode.CORRUPT_LOG_LINE,
                                f"Blank line in judge record log at line {line_number}",
                                line_number,
                            )
                        existing_id = _read_record_id(line, line_number)
                        if existing_id == record.record_id:
                            raise JudgeRecordPersistenceError(
                                JudgeRecordPersistenceErrorCode.DUPLICATE_RECORD_ID,
                                f"Duplicate judge record_id: {record.record_id}",
                                line_number,
                            )

            serialized = record.model_dump_json()
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(serialized + "\n")
                stream.flush()
                os.fsync(stream.fileno())

