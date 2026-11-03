"""Reserved diagnostics remain deterministic and separate from experimental data."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import run_reserved_requirement_cases as reserved


class ReservedRequirementTests(unittest.TestCase):
    def test_manifest_sealed_and_each_candidate_has_three_blinded_prompts(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)
            plan, queue, mapping, candidates = reserved.load(path, path)
            self.assertEqual(plan['planned'], 18)
            self.assertEqual(len({r['evaluation_id'] for r in queue}), 18)
            self.assertEqual(len(candidates), 6)
            self.assertEqual(set(candidates), {r['job_id'] for r in mapping.values()})
            for name in candidates:
                self.assertEqual(sum(r['job_id']==name for r in mapping.values()),3)
            self.assertNotIn('Cartões numerados', candidates['omission'])
            self.assertNotIn('quadro', candidates['omission'])
            self.assertIn('35 minutos',candidates['duration_contradiction'])
            self.assertEqual(reserved.load(path,path)[0], plan)
            manifest = path/'reserved_manifest.json'
            data=json.loads(manifest.read_text(encoding='utf-8'))
            data['definition']['repetitions']=1
            manifest.write_text(json.dumps(data),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'changed'):
                reserved.load(path,path)

    def test_incomplete_diagnostics_never_report_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary);reserved.prepare(path)
            (path/'summary.v2.json').write_text(json.dumps({'completed':0,'statuses':{},'responses':[]}),encoding='utf-8')
            result=reserved.report(path)
            self.assertEqual(result['check_counts'],{'incomplete':6})
