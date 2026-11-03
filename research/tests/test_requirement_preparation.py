"""Offline queue binds new prompts to saved responses without changing inputs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_requirement_judgments import prepare
from experiment.judge_contract_v2 import PROMPT_VERSION, SCHEMA_VERSION


class RequirementPreparationTests(unittest.TestCase):
    def test_saved_pilot_preparation_is_blinded_reproducible_and_read_only(self):
        source = ROOT / 'artifacts/pilot-qwen3-local'
        original = (source / 'generations.jsonl').read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            report = prepare(source, output)
            queue_bytes = (output / 'queue.jsonl').read_bytes()
            queue = [json.loads(line) for line in queue_bytes.splitlines()]
            mapping = [json.loads(line) for line in (output / 'mapping.jsonl').read_text().splitlines()]
            self.assertEqual(report['prepared_judgments'], 81)
            self.assertEqual(report['api_calls'], 0)
            self.assertEqual(report['judgments_executed'], 0)
            self.assertEqual(report['source_log_sha256'], sha256(original).hexdigest())
            self.assertEqual(len({r['evaluation_id'] for r in queue}), 81)
            self.assertEqual({r['evaluation_id'] for r in queue}, {r['evaluation_id'] for r in mapping})
            self.assertEqual(report['prompt_version'], PROMPT_VERSION)
            for row in queue:
                self.assertNotIn('condition', row)
                self.assertNotIn('generator_id', row)
                self.assertEqual(row['prompt_sha256'], sha256(row['prompt'].encode()).hexdigest())
                self.assertTrue(row['body']['text']['format']['strict'])
                schema = row['body']['text']['format']['schema']
                self.assertEqual(schema['properties']['schema_version']['enum'], [SCHEMA_VERSION])
            prepare(source, output)
            self.assertEqual(queue_bytes, (output / 'queue.jsonl').read_bytes())
        self.assertEqual(original, (source / 'generations.jsonl').read_bytes())

    def test_executor_provenance_is_independent_of_windows_line_endings(self):
        from run_requirement_judgments import load
        source = ROOT / 'artifacts/pilot-qwen3-local'
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            prepare(source, output)
            for name in ('queue.jsonl', 'mapping.jsonl', 'preparation_report.json'):
                path = output / name
                path.write_bytes(path.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
            plan, *_ = load(source, output)
            self.assertEqual(plan['planned'], 81)
            queue = output / 'queue.jsonl'
            rows = list(map(json.loads, queue.read_text(encoding='utf-8').splitlines()))
            rows[0]['body']['model'] = 'tampered'
            queue.write_text(''.join(json.dumps(row)+'\n' for row in rows), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'provenance mismatch'):
                load(source, output)
