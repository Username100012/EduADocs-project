"""End-to-end audit using synthetic outputs and temporary logs only."""

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest

from tests.test_llm_judge_record import (
    EVALUATION_ID, CANDIDATE, payload, valid_raw_response,
)
from experiment.judge_audit import OfflineJudgeAudit


ROOT = Path(__file__).resolve().parents[1]


class OfflineJudgeAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.log = Path(self.temp.name) / "audit.jsonl"
        self.audit = OfflineJudgeAudit(
            ROOT, ROOT / "experiments/judge_execution_manifest.v1.json", self.log
        )

    def capture(self, raw=None, attempt=1, **overrides):
        arguments = dict(
            evaluation_id=EVALUATION_ID, payload=payload(), candidate=CANDIDATE,
            raw_response=valid_raw_response() if raw is None else raw,
            task_id="task-001", condition="c0",
            generation_execution_id="generation-001", repetition=1, attempt=attempt,
        )
        arguments.update(overrides)
        return self.audit.capture(**arguments)

    def test_success_round_trip_and_blinded_prompt(self):
        entry = self.capture()
        self.audit.append(entry, payload())
        saved = json.loads(self.log.read_text(encoding="utf-8"))
        self.assertEqual(saved["manifest_hash"], self.audit.manifest.manifest_hash)
        self.assertEqual(saved["record"]["raw_response"], valid_raw_response())
        prompt = saved["record"]["prompt"]["text"]
        for marker in ("generation-001", "task-001", '"condition"', "gpt-5.4"):
            self.assertNotIn(marker, prompt)

    def test_failed_attempt_then_success_preserves_both(self):
        self.audit.append(self.capture(raw="invalid"), payload())
        self.audit.append(self.capture(attempt=2), payload())
        rows = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual([r["attempt"] for r in rows], [1, 2])
        self.assertEqual([r["record"]["status"] for r in rows], ["error", "success"])

    def test_duplicate_retry_after_success_and_skipped_attempt_are_rejected(self):
        with self.assertRaises(ValueError):
            self.audit.append(self.capture(attempt=2), payload())
        first = self.capture()
        self.audit.append(first, payload())
        original = self.log.read_bytes()
        for entry in (first, self.capture(attempt=2)):
            with self.assertRaises(ValueError):
                self.audit.append(entry, payload())
        self.assertEqual(self.log.read_bytes(), original)

    def test_tampered_raw_response_and_manifest_link_are_rejected(self):
        entry = self.capture()
        forged = entry.model_copy(update={
            "record": entry.record.model_copy(update={"raw_response": "invalid"})
        })
        for changed in (forged, entry.model_copy(update={"manifest_hash": "0" * 64})):
            with self.assertRaises(ValueError):
                self.audit.append(changed, payload())
        self.assertFalse(self.log.exists())

    def test_changed_retry_input_and_out_of_policy_repetition_are_rejected(self):
        self.audit.append(self.capture(raw="invalid"), payload())
        with self.assertRaises(ValueError):
            self.audit.append(self.capture(attempt=2, candidate="Different"), payload())
        with self.assertRaises(ValueError):
            self.capture(repetition=4)
        with self.assertRaises(ValueError):
            self.capture(attempt=3)

    def test_incomplete_existing_tail_is_preserved(self):
        self.log.write_text('{"broken":', encoding="utf-8")
        original = self.log.read_bytes()
        with self.assertRaises(ValueError):
            self.audit.append(self.capture(), payload())
        self.assertEqual(self.log.read_bytes(), original)

    def test_tampered_manifest_seal_is_rejected(self):
        manifest = Path(self.temp.name) / "manifest.json"
        manifest.write_bytes((ROOT / "experiments/judge_execution_manifest.v1.json").read_bytes())
        manifest.with_suffix(".canonical.sha256").write_text("0" * 64)
        with self.assertRaises(ValueError):
            OfflineJudgeAudit(ROOT, manifest, self.log)

    def test_concurrent_duplicate_is_written_only_once(self):
        entry = self.capture()

        def persist():
            try:
                self.audit.append(entry, payload())
                return "saved"
            except ValueError:
                return "rejected"

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: persist(), range(2)))
        self.assertCountEqual(outcomes, ["saved", "rejected"])
        self.assertEqual(len(self.log.read_text().splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
