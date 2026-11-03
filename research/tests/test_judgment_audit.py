"""Offline arithmetic checks distinguish demonstrable errors from caveats."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_judgments import arithmetic_alert, audit


class JudgmentAuditTests(unittest.TestCase):
    def test_false_addition_claim_requires_declared_target(self):
        result = arithmetic_alert('A soma (8+22+10) excede a duração declarada de 40 minutos.', 'Duração: 40 minutos')
        self.assertEqual(result[0]['computed_sum'], 40)
        self.assertEqual(result[0]['declared_minutes'], 40)
        self.assertEqual(arithmetic_alert('8+22+10 excede 40 minutos.', 'Sem duração.'), [])

    def test_true_claim_and_negated_claim_are_not_errors(self):
        self.assertEqual(arithmetic_alert('8+32+10 excede 40 minutos.', 'Duração: 40 minutos'), [])
        self.assertEqual(arithmetic_alert('8+22+10 não excede 40 minutos.', 'Duração: 40 minutos'), [])
        self.assertEqual(arithmetic_alert('Há pequenas lacunas.', 'Duração: 40 minutos'), [])

    def test_audit_preserves_inputs_and_rejects_changed_log(self):
        source = ROOT / 'artifacts/pilot-qwen3-local'
        if not (source / 'judgment_summary.json').exists():
            self.skipTest('saved judgments absent')
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            names = ('judge_queue.jsonl', 'judge_mapping.jsonl', 'generations.jsonl', 'judgments.jsonl', 'judgment_summary.json')
            for name in names:
                shutil.copyfile(source / name, directory / name)
            before = {name: (directory / name).read_bytes() for name in names}
            report = audit(directory)
            self.assertEqual(len(report['distributions']), 12)
            self.assertEqual(len(report['task_comparisons']), 12)
            self.assertEqual(sum(d['n'] for d in report['distributions']), 324)
            self.assertEqual(report['api_calls'], 0)
            self.assertFalse(report['source_scores_changed'])
            self.assertEqual(before, {name: (directory / name).read_bytes() for name in names})
            path = directory / 'judgment_summary.json'
            summary = json.loads(path.read_text(encoding='utf-8'))
            summary['source_judgments_sha256'] = 'bad'
            path.write_text(json.dumps(summary), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'stale'):
                audit(directory)
