"""Conservative costs account for repetitions and avoid double-counting thinking."""
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from budget_gemini_main import estimate,build_plan

class GeminiBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads((ROOT/'experiments/main_config.json').read_text(encoding='utf-8'))
        cls.counts={sha256(j['prompt']['text'].encode()).hexdigest():10
                    for j in build_plan(cls.config) if j['generator_id']=='gemini'}

    def test_all_repetitions_and_output_ceiling_are_included_once(self):
        result=estimate(self.config,self.counts)
        self.assertEqual(result['calls'],108)
        self.assertEqual(result['input_tokens_total'],1080)
        self.assertEqual(result['output_tokens_total_cap'],108*4096)
        self.assertEqual([r['calls'] for r in result['by_condition']],[36,36,36])
        expected=(Decimal(1080)*Decimal('.75')+Decimal(108*4096)*Decimal('3.75'))/Decimal(1_000_000)
        self.assertEqual(Decimal(result['usd_at_output_cap']),expected)
        self.assertGreaterEqual(Decimal(result['conservative_brl']),expected*6*Decimal('1.25'))
        self.assertTrue(result['fits_budget'])
        self.assertEqual(Decimal(result['conservative_brl'])+Decimal(result['remaining_brl_after_reserve']),Decimal(result['available_brl']))

    def test_future_price_stress_and_insufficient_budget(self):
        normal=estimate(self.config,self.counts)
        doubled=estimate(self.config,self.counts,price_multiplier='2')
        self.assertEqual(Decimal(doubled['usd_at_output_cap']),2*Decimal(normal['usd_at_output_cap']))
        self.assertFalse(estimate(self.config,self.counts,available='1')['fits_budget'])
        self.assertFalse(estimate(self.config,{k:1_000_000 for k in self.counts})['fits_budget'])

    def test_missing_invalid_counts_and_assumptions_are_rejected(self):
        for values in ({},{k:True for k in self.counts},{k:0 for k in self.counts}):
            with self.assertRaises(ValueError):estimate(self.config,values)
        with self.assertRaises(ValueError):estimate(self.config,self.counts,exchange='0')
