"""Tables keep denominators, incomplete triplets and nominal categories explicit."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import report_requirement_results as reports
from test_requirement_contract_v2 import fixture

class RequirementReportTests(unittest.TestCase):
    def test_failed_judgment_never_becomes_zero_or_complete_triplet(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)
            ids=['a','b','c'];plan={'event':'plan'}
            mapping={e:{'condition':'c1','job_id':'job'} for e in ids}
            events=[plan]
            for e in ids:
                events.extend([{'event':'started','evaluation_id':e},
                    {'event':'result','evaluation_id':e,'status':'api_error' if e=='c' else 'success',
                     'validated':None if e=='c' else fixture()}])
            (path/'judgments.v2.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events),encoding='utf-8')
            (path/'generations.jsonl').write_text(json.dumps({'jobs':[{'job_id':'job','condition':'c1',
                'payload':{name:'test' for name in fixture()['requirements']}}]})+'\n',encoding='utf-8')
            with patch.object(reports,'load',return_value=(plan,[{}]*3,mapping,{})):
                result=reports.report(path,path)
            self.assertEqual(result['operational'][0]['valid'],2)
            self.assertEqual(result['operational'][0]['complete_triplets'],0)
            self.assertEqual(result['requirements'][0]['uncertain'],2)
            self.assertIsNone(result['secondary_scores'][0]['median_of_response_medians'])

    def test_recovered_authentication_attempt_is_counted_once(self):
        import recover_requirement_auth_failures as recovery
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp);extra=path/'recovery';extra.mkdir()
            ids=['a','b','c'];plan={'event':'plan'};recovery_plan={'event':'plan','attempt':2}
            mapping={e:{'condition':'c1','job_id':'job'} for e in ids}
            events=[plan]
            for eid in ids:
                events.extend([{'event':'started','evaluation_id':eid},{'event':'result','evaluation_id':eid,
                    'status':'api_error' if eid=='c' else 'success','http_status':401 if eid=='c' else 200,
                    'validated':None if eid=='c' else fixture()}])
            (path/'judgments.v2.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events),encoding='utf-8')
            recovered=[recovery_plan,{'event':'started','evaluation_id':'c'},
                {'event':'result','evaluation_id':'c','status':'success','validated':fixture()}]
            (extra/'judgments.v2.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in recovered),encoding='utf-8')
            (path/'generations.jsonl').write_text(json.dumps({'jobs':[{'job_id':'job','condition':'c1',
                'payload':{name:'test' for name in fixture()['requirements']}}]})+'\n',encoding='utf-8')
            with patch.object(reports,'load',return_value=(plan,[{}]*3,mapping,{})), patch.object(recovery,'load',return_value=(recovery_plan,[],{'c':mapping['c']},{})):
                result=reports.report(path,path,extra)
            self.assertEqual(result['operational_attempts'],4)
            self.assertEqual(result['completed'],3)
            self.assertEqual(result['operational'][0]['complete_triplets'],1)
            self.assertEqual(result['requirements'][0]['uncertain'],3)

    def test_generators_are_never_pooled_into_one_condition_score(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp);plan={'event':'plan'};events=[plan];mapping={};jobs=[]
            for generator,score in [('gemini',4),('qwen3',1)]:
                job=generator+':job'
                jobs.append({'job_id':job,'task_id':'task-001','generator_id':generator,'condition':'c1',
                    'payload':{name:'test' for name in fixture()['requirements']}})
                for rep in range(3):
                    eid=f'{generator}:{rep}';mapping[eid]={'generator_id':generator,'condition':'c1','job_id':job}
                    value=fixture()
                    for criterion in value['assessments'].values():criterion['score']=score
                    events.extend([{'event':'started','evaluation_id':eid},
                        {'event':'result','evaluation_id':eid,'status':'success','validated':value}])
            (path/'judgments.v2.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events),encoding='utf-8')
            (path/'generations.jsonl').write_text(json.dumps({'config':{'study_phase':'main'},'jobs':jobs})+'\n',encoding='utf-8')
            with patch.object(reports,'load',return_value=(plan,[{}]*6,mapping,{})):
                result=reports.report(path,path)
            self.assertEqual(len(result['operational']),2)
            aligned={r['generator_id']:r['median_of_task_medians'] for r in result['secondary_scores'] if r['criterion']=='instructional_alignment'}
            self.assertEqual(aligned,{'gemini':4,'qwen3':1})
