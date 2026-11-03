"""Synthetic mutation isolation and ties must not masquerade as sensitivity."""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_judge_sensitivity import build_plan, execute, summarize
from experiment.judge_prompt import JUDGE_CRITERIA, JUDGE_RESPONSE_SCHEMA_VERSION, JUDGE_RUBRIC_VERSION


class JudgeSensitivityTests(unittest.TestCase):
    def test_sol_preserves_all_texts_and_changes_only_compatible_configuration(self):
        previous = build_plan()
        sol = build_plan("gpt-6.1-sol")
        self.assertEqual(previous['expected_relations'], sol['expected_relations'])
        for old, new in zip(previous['jobs'], sol['jobs']):
            for field in ('evaluation_id', 'candidate', 'candidate_sha256', 'prompt_sha256', 'payload', 'kind', 'repetition'):
                self.assertEqual(old[field], new[field])
            self.assertEqual(old['body']['input'], new['body']['input'])
            self.assertEqual(old['body']['text'], new['body']['text'])
            self.assertNotIn('temperature', new['body'])
            self.assertNotIn('top_p', new['body'])
            self.assertEqual(new['body']['reasoning'], {'effort': 'low'})
            self.assertEqual(new['body']['max_output_tokens'], 4096)
        self.assertEqual(build_plan(), previous)

    def test_isolated_mutations_and_complete_plan(self):
        plan = build_plan()
        self.assertEqual(len(plan["jobs"]), 36)
        self.assertEqual(len({j["evaluation_id"] for j in plan["jobs"]}), 36)
        self.assertEqual(sum(plan["baseline_stage_minutes"]), 50)
        self.assertEqual(sum(plan["time_variant_stage_minutes"]), 100)
        for task in {j["task_id"] for j in plan["jobs"]}:
            texts = {j["kind"]: j["candidate"] for j in plan["jobs"] if j["task_id"] == task}
            baseline = texts["baseline"]
            self.assertEqual(texts["omission"], "\n".join(l for l in baseline.splitlines() if not l.startswith("Materiais:")))
            self.assertEqual(texts["time_contradiction"].replace("(70 minutos)", "(20 minutos)"), baseline)
            self.assertEqual(texts["misalignment"].splitlines()[:-1], baseline.splitlines()[:-1])

    def fake(self, *args, **kwargs):
        body = kwargs["json"]
        eid = re.search(r'eval-[a-f0-9]{32}', body["input"])[0]
        data = {"schema_version": JUDGE_RESPONSE_SCHEMA_VERSION, "rubric_version": JUDGE_RUBRIC_VERSION,
                "evaluation_id": eid, "assessments": {c: {"score": 4, "justification": "Fixture constante."} for c in JUDGE_CRITERIA}}
        response = Mock(status_code=200, ok=True, headers={})
        response.json.return_value = {"model": body["model"], "status": "completed", "usage": {"input_tokens": 10, "output_tokens": 5},
                                      "output": [{"content": [{"type": "output_text", "text": json.dumps(data)}]}]}
        return response

    def test_constant_scores_are_nine_ties_not_successful_sensitivity(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            post = Mock(side_effect=self.fake)
            with redirect_stdout(StringIO()):
                execute(directory, "fake", post=post)
                before = (directory / "judgments.jsonl").read_bytes()
                execute(directory, "fake", post=post)
            self.assertEqual(post.call_count, 36)
            self.assertEqual((directory / "judgments.jsonl").read_bytes(), before)
            report = summarize(directory)
            self.assertEqual(report["outcomes"], {"tie": 9})
            self.assertTrue(all(r["strict_decrease_detected"] is False for r in report["relations"]))
            events = [json.loads(line) for line in before.decode().splitlines()]
            next(e for e in events if e["event"] == "result")["status"] = "api_error"
            (directory / "judgments.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
            report = summarize(directory)
            self.assertGreater(report["outcomes"].get("incomplete", 0), 0)
            self.assertTrue(any(r["delta"] is None for r in report["relations"]))

    def test_interruption_is_not_retried(self):
        with tempfile.TemporaryDirectory() as temp:
            post = Mock(side_effect=KeyboardInterrupt)
            with self.assertRaises(KeyboardInterrupt):
                execute(Path(temp), "fake", post=post)
            with self.assertRaisesRegex(ValueError, "unresolved"):
                execute(Path(temp), "fake", post=post)
            self.assertEqual(post.call_count, 1)
