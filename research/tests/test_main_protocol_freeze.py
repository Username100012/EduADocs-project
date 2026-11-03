"""Local seals block drift before output/network; no real provider calls."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'src'))
from experiment import main_protocol as protocol
from experiment.pilot_runner import build_plan,run_pilot
from prepare_requirement_judgments import prepare as prepare_queue


class MainFreezeTests(unittest.TestCase):
    def make_fixture(self, root):
        config=json.loads((ROOT/'experiments/main_config.json').read_text(encoding='utf-8'))
        (root/'control.txt').write_text('source v1',encoding='utf-8')
        config['protocol_version']='eduadocs-main-v1.0.0';config['status']='ready_for_collection'
        config['freeze']={'artifact_sha256':{'control.txt':sha256((root/'control.txt').read_bytes()).hexdigest()},
            'catalog_sha256':protocol.canonical_hash(config['tasks']),
            'prompt_plan_sha256':protocol.canonical_hash(build_plan(config))}
        path=root/'main.json';path.write_text(json.dumps(config,ensure_ascii=False),encoding='utf-8')
        path.with_suffix('.json.sha256').write_text(sha256(path.read_bytes()).hexdigest()+'\n',encoding='utf-8')
        return path

    def test_configuration_and_source_drift_are_detected(self):
        with tempfile.TemporaryDirectory() as temporary,patch.object(protocol,'ARTIFACTS',('control.txt',)):
            root=Path(temporary);path=self.make_fixture(root)
            protocol.verify_frozen(path,root=root)
            (root/'control.txt').write_text('source v2',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'artifact changed'):
                protocol.verify_frozen(path,root=root)
            path=self.make_fixture(root)
            path.write_text(path.read_text(encoding='utf-8')+' ',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'checksum'):
                protocol.verify_frozen(path,root=root)

    def test_unsealed_ready_configuration_cannot_start_live_calls(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);path=self.make_fixture(root)
            path.with_suffix('.json.sha256').unlink()
            output=root/'no-output'
            with patch('requests.post') as post,patch('requests.get') as get:
                with self.assertRaisesRegex(ValueError,'checksum'):
                    run_pilot(path,output,simulated=False)
                post.assert_not_called();get.assert_not_called()
            self.assertFalse(output.exists())

    def test_main_offline_flow_prepares_648_judgments_without_network(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            with patch('requests.post') as post,patch('requests.get') as get:
                result=run_pilot(ROOT/'experiments/main_config.json',root/'simulated')
                report=prepare_queue(root/'simulated',root/'queue')
                self.assertEqual(result['completed'],216)
                self.assertEqual(report['prepared_judgments'],648)
                self.assertTrue(report['simulated_generations'])
                self.assertEqual(report['api_calls'],0)
                from run_requirement_judgments import load
                with self.assertRaisesRegex(ValueError,'simulated'):
                    load(root/'simulated',root/'queue')
                self.assertEqual(len({json.loads(line)['evaluation_id'] for line in (root/'queue/queue.jsonl').read_text(encoding='utf-8').splitlines()}),648)
                post.assert_not_called();get.assert_not_called()
