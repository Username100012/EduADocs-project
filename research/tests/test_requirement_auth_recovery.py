"""Only historical authentication failures can be retried, in a separate log."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import recover_requirement_auth_failures as recovery

class AuthRecoveryTests(unittest.TestCase):
    def test_only_two_authentication_errors_are_eligible(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);original=root/'judge-contract-v2-preparation';original.mkdir()
            events=[{'event':'plan'}]+[{'event':'result','evaluation_id':e,'status':'api_error','http_status':401} for e in ('a','b')]
            log=original/'judgments.v2.jsonl'
            log.write_text(''.join(json.dumps(e)+'\n' for e in events),encoding='utf-8')
            data=({'event':'plan'},[{'evaluation_id':e} for e in ('a','b','c')],
                  {e:{'job_id':'job'} for e in ('a','b','c')},{'job':'candidate'})
            with patch.object(recovery,'load_original',return_value=data):
                plan,queue,mapping,_=recovery.load(root,root/'recovery')
                self.assertEqual(plan['attempt'],2)
                self.assertEqual({r['evaluation_id'] for r in queue},{'a','b'})
                self.assertEqual(set(mapping),{'a','b'})
                events[1]['status']='validation_error'
                log.write_text(''.join(json.dumps(e)+'\n' for e in events),encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'two historical'):
                    recovery.load(root,root/'recovery')
