"""Offline execution verifies resume, blinding and failure retention."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_judgments import execute, load_plan
from summarize_judgments import summarize


class JudgmentRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        source = ROOT / "artifacts/pilot-qwen3-local"
        if not (source / "judge_queue.jsonl").exists():
            self.skipTest("saved pilot absent")
        for name in ("judge_queue.jsonl", "judge_mapping.jsonl", "generations.jsonl"):
            shutil.copyfile(source / name, self.directory / name)

    def fake(self, *args, **kwargs):
        from experiment.judge_prompt import JUDGE_CRITERIA, JUDGE_RESPONSE_SCHEMA_VERSION, JUDGE_RUBRIC_VERSION
        import re
        body = kwargs["json"]
        eid = re.search(r'eval-[a-f0-9]{32}', body["input"])[0]
        data = {"schema_version": JUDGE_RESPONSE_SCHEMA_VERSION, "rubric_version": JUDGE_RUBRIC_VERSION,
                "evaluation_id": eid, "assessments": {c: {"score": 3, "justification": "Evidência de teste."} for c in JUDGE_CRITERIA}}
        response = Mock(status_code=200, ok=True, headers={})
        response.json.return_value = {"model": body["model"], "status": "completed", "usage": {"input_tokens": 20, "output_tokens": 10},
                                      "output": [{"content": [{"type": "output_text", "text": json.dumps(data)}]}]}
        self.assertNotIn("qwen3:pilot-", body["input"])
        return response

    def test_validated_resume_never_duplicates(self):
        post = Mock(side_effect=self.fake)
        self.assertEqual(execute(self.directory, "fake", post=post, max_jobs=1)["success"], 1)
        prefix = (self.directory / "judgments.jsonl").read_bytes()
        self.assertEqual(execute(self.directory, "fake", post=post, max_jobs=1)["success"], 2)
        self.assertEqual(post.call_count, 2)
        self.assertTrue((self.directory / "judgments.jsonl").read_bytes().startswith(prefix))

    def test_interrupted_call_blocks_resume(self):
        post = Mock(side_effect=KeyboardInterrupt)
        with self.assertRaises(KeyboardInterrupt):
            execute(self.directory, "fake", post=post)
        with self.assertRaisesRegex(ValueError, "unresolved"):
            execute(self.directory, "fake", post=post)
        self.assertEqual(post.call_count, 1)

    def test_changed_prompt_blocks_before_call(self):
        path = self.directory / "judge_queue.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        rows[0]["prompt"] += "changed"
        path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        post = Mock()
        with self.assertRaisesRegex(ValueError, "evidence"):
            execute(self.directory, "fake", post=post)
        post.assert_not_called()

    def test_full_summary_and_failed_judgment_is_not_scored_zero(self):
        post = Mock(side_effect=self.fake)
        with redirect_stdout(StringIO()):
            self.assertEqual(execute(self.directory, "fake", post=post)["success"], 81)
            original = (self.directory / "judgments.jsonl").read_bytes()
            execute(self.directory, "fake", post=post)
        self.assertEqual(post.call_count, 81)
        self.assertEqual((self.directory / "judgments.jsonl").read_bytes(), original)
        report = summarize(self.directory)
        self.assertEqual(len(report["response_medians"]), 108)
        self.assertEqual(len(report["summaries"]), 48)
        for row in report["summaries"]:
            self.assertEqual(row["median"], 3)
            self.assertEqual(row["maximum_within_response_range"], 0)
        events = [json.loads(line) for line in original.decode().splitlines()]
        first = next(e for e in events if e["event"] == "result")
        first.update(status="api_error", record=None, raw_text=None)
        (self.directory / "judgments.jsonl").write_text(
            "".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
        report = summarize(self.directory)
        self.assertEqual(report["successful_judgments"], 80)
        self.assertEqual(sum(r["complete_triplet"] for r in report["response_medians"]), 104)
        self.assertTrue(all(r["median"] in (3, None) for r in report["response_medians"]))
