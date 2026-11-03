"""Reporting checks: missing results, nominal observations and reported cost."""
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from summarize_main_observations import aggregate,reported_google_cost,LABELS

class MainObservationSummaryTests(unittest.TestCase):
    def row(self):
        return {'status':'success','content_sha256':'same-text','word_count':20,
            'operational':{'latency_ms':200,'input_tokens':10,'output_tokens':50},
            'observation':{'fields':{k:{'observation':'detected'} for k in LABELS},
              'duration':{'declared_matches_target':None,'schedule_matches_target':None,
                'target_mismatch_detected':None,'internal_inconsistency_detected':None,
                'declared':[],'clock_schedule_minutes':None}}}

    def test_timeout_stays_missing_and_repetitions_do_not_become_unique_texts(self):
        first=self.row();second=deepcopy(first);second['operational']['latency_ms']=400
        failure={'status':'error','observation':None,'operational':None,'content_sha256':None}
        result=aggregate([first,second,failure],3)
        self.assertEqual(result['analyzable_texts'],2)
        self.assertEqual(result['results_without_text'],1)
        self.assertEqual(result['unique_texts'],1)
        self.assertEqual(result['operational']['latency_ms']['median'],300)
        self.assertEqual(result['operational']['latency_ms']['available'],2)
        self.assertEqual(result['fields']['topic']['denominator'],2)
        self.assertEqual(result['duration']['target_mismatch_detected']['unknown'],2)
        self.assertIsNone(result['reported_google_cost_estimate']['usd_sum'])

    def test_empty_field_is_separate_from_not_detected_and_from_missing_response(self):
        first=self.row();second=self.row()
        first['observation']['fields']['materials']['observation']='empty'
        second['observation']['fields']['materials']['observation']='not_detected'
        field=aggregate([first,second],2)['fields']['materials']
        self.assertEqual(field['counts'],{'detected':0,'empty':1,'not_detected':1})
        self.assertEqual(sum(field['proportions'].values()),1)

    def test_cost_counts_thinking_once_and_rejects_unknown_or_inconsistent_usage(self):
        price={'input_usd_per_million_tokens':.75,'output_usd_per_million_tokens_including_thinking':3.75}
        response={'provider':'google','input_tokens':100,'output_tokens':200,'raw_metadata':{'total_tokens':350}}
        expected=(Decimal(100)*Decimal('.75')+Decimal(250)*Decimal('3.75'))/Decimal(1_000_000)
        self.assertEqual(Decimal(reported_google_cost(response,price)),expected)
        response['raw_metadata']['total_tokens']=None
        self.assertIsNone(reported_google_cost(response,price))
        response['raw_metadata']['total_tokens']=250
        self.assertIsNone(reported_google_cost(response,price))
        self.assertIsNone(reported_google_cost(None,price))
