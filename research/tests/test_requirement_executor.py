"""Execution safety and aggregation checked with a fake transport only."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_requirement_judgments as runner
from test_requirement_contract_v2 import fixture, CANDIDATE


class RequirementExecutorTests(unittest.TestCase):
    def plan(self):
        ids = ['eval-' + c * 32 for c in 'abc']
        return ({'event': 'plan', 'planned': 3},
                [{'evaluation_id': e, 'body': {'model': 'test', 'input': e}} for e in ids],
                {e: {'job_id': 'job'} for e in ids}, {'job': CANDIDATE})

    def post(self, url, *, headers, json, timeout):
        data = fixture(); data['evaluation_id'] = json['input']
        return type('Response', (), {'ok': True, 'status_code': 200, 'headers': {},
            'json': lambda self: {'model': 'test', 'status': 'completed',
            'output': [{'content': [{'type': 'output_text', 'text': __import__('json').dumps(data)}]}]}})()

    def test_resume_does_not_repeat_and_only_complete_triplets_have_medians(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner, 'load', return_value=self.plan()):
            directory = Path(temporary)
            first = runner.execute(directory, directory, 'test-secret', max_jobs=1, post=self.post)
            self.assertEqual(first['completed'], 1)
            self.assertIsNone(first['responses'][0]['assessments']['textual_coherence']['median'])
            final = runner.execute(directory, directory, 'test-secret', max_jobs=3, post=self.post)
            self.assertEqual(final['completed'], 3)
            self.assertTrue(final['responses'][0]['complete_triplet'])
            self.assertEqual(final['responses'][0]['requirements']['topic']['frequencies'], {'uncertain': 3})
            def forbidden(*args, **kwargs):
                self.fail('completed calls repeated')
            runner.execute(directory, directory, 'test-secret', max_jobs=3, post=forbidden)

    def test_invalid_json_stops_the_batch_and_records_classified_error(self):
        def invalid(*args, **kwargs):
            response = self.post(*args, **kwargs)
            response.json = lambda: {'model': 'test', 'status': 'completed',
                'output': [{'content': [{'type': 'output_text', 'text': '{}'}]}]}
            return response
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner, 'load', return_value=self.plan()):
            directory = Path(temporary)
            report = runner.execute(directory, directory, 'test-secret', max_jobs=3, post=invalid)
            self.assertEqual(report['completed'], 1)
            self.assertEqual(report['statuses'], {'validation_error': 1})
            events = list(map(json.loads, (directory / 'judgments.v2.jsonl').read_text().splitlines()))
            self.assertEqual(events[-1]['error']['code'], 'schema_error')
            events.append({'event': 'started', 'evaluation_id': self.plan()[1][1]['evaluation_id']})
            (directory / 'judgments.v2.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
            with self.assertRaisesRegex(ValueError, 'unresolved'):
                runner.execute(directory, directory, 'test-secret', max_jobs=3, post=invalid)

    def test_parallel_wave_finishes_inflight_calls_then_stops_on_failure(self):
        def invalid(*args, **kwargs):
            response = self.post(*args, **kwargs)
            response.json = lambda: {'model': 'test', 'status': 'completed',
                'output': [{'content': [{'type': 'output_text', 'text': '{}'}]}]}
            return response
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner, 'load', return_value=self.plan()):
            path = Path(temporary)
            result = runner.execute(path,path,'test-secret',max_jobs=3,workers=2,post=invalid)
            self.assertEqual(result['completed'],2)
            events=list(map(json.loads,(path/'judgments.v2.jsonl').read_text(encoding='utf-8').splitlines()))
            self.assertEqual(sum(e['event']=='started' for e in events),2)
            self.assertEqual(sum(e['event']=='result' for e in events),2)

    def test_explicit_continuation_never_repairs_or_repeats_validation_failures(self):
        def invalid(*args, **kwargs):
            response=self.post(*args,**kwargs)
            response.json=lambda:{'model':'test','status':'completed','output':[{'content':[{'type':'output_text','text':'{}'}]}]}
            return response
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner,'load',return_value=self.plan()):
            path=Path(temporary)
            result=runner.execute(path,path,'test-secret',max_jobs=3,workers=2,post=invalid,continue_validation_errors=True)
            self.assertEqual(result['completed'],3)
            self.assertEqual(result['statuses'],{'validation_error':3})
