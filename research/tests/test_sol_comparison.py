"""Price arithmetic and baseline comparison must not silently rewrite data."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from compare_judge_sensitivity import estimate_cost, load


class SolComparisonTests(unittest.TestCase):
    def test_cache_reads_and_writes_are_separate(self):
        rates = {'input': 2, 'cached_input': .1, 'cache_write': 2.5, 'output': 10}
        usage = {'input_tokens': 100, 'output_tokens': 50,
                 'input_tokens_details': {'cached_tokens': 20, 'cache_write_tokens': 30}}
        self.assertAlmostEqual(estimate_cost(usage, rates), (50*2 + 20*.1 + 30*2.5 + 50*10)/1e6)
        with self.assertRaises(ValueError):
            estimate_cost({**usage, 'input_tokens': 10}, rates)
        with self.assertRaises(ValueError):
            estimate_cost(usage, {**rates, 'cache_write': None})

    def test_loading_reference_does_not_overwrite_legacy_outputs(self):
        directory = ROOT / 'artifacts/judge-sensitivity-v1'
        if not (directory / 'report.json').exists():
            self.skipTest('legacy collection absent')
        names = ('report.json', 'RESULTS.md', 'judgments.jsonl')
        before = {n: (directory / n).read_bytes() for n in names}
        summary, _, _ = load(directory, 'gpt-5.4-mini-2026-03-17')
        self.assertEqual(summary['completed'], 36)
        self.assertEqual(before, {n: (directory / n).read_bytes() for n in names})
