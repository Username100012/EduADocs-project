"""Append-only JSONL persistence for reproducible executions."""

from pathlib import Path

from filelock import FileLock

from experiment.models import ExecutionRecord


DEFAULT_LOG_PATH = Path(__file__).resolve().parents[2] / "data" / "executions.jsonl"


class ExecutionLogger:
    """Persist one JSON object per line under an inter-process file lock."""

    def __init__(self, path: Path | str = DEFAULT_LOG_PATH) -> None:
        self.path = Path(path)

    def append(self, record: ExecutionRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock = FileLock(str(self.path) + ".lock")
        with lock:
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(record.model_dump_json() + "\n")
