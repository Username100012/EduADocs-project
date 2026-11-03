"""Verify the controlled transformations, not hypothetical judge scores."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from experiment.judge_metamorphic import load_metamorphic_pairs, metamorphic_suite_hash


class MetamorphicCaseTests(unittest.TestCase):
    def test_suite_matches_preserved_hash(self):
        path = ROOT / "experiments/judge_metamorphic_cases.v1.json"
        seal = ROOT / "experiments/judge_metamorphic_cases.v1.sha256"
        self.assertEqual(metamorphic_suite_hash(path), seal.read_text().split()[0])

    def test_twelve_pairs_with_unique_ids_and_four_transformations(self):
        pairs = load_metamorphic_pairs(ROOT / "experiments/judge_metamorphic_cases.v1.json")
        self.assertEqual(len(pairs), 12)
        self.assertEqual(len({p.case_id for p in pairs}), 12)
        for kind in ("consistency", "verbosity", "omission", "misalignment"):
            self.assertEqual(sum(p.kind == kind for p in pairs), 3)

    def test_each_transformation_preserves_the_unmodified_sections(self):
        pairs = load_metamorphic_pairs(ROOT / "experiments/judge_metamorphic_cases.v1.json")
        for pair in pairs:
            before, after = pair.baseline.splitlines(), pair.variant.splitlines()
            with self.subTest(case=pair.case_id):
                if pair.kind == "consistency":
                    self.assertEqual(pair.baseline, pair.variant)
                elif pair.kind == "verbosity":
                    self.assertEqual(after[:-1], before)
                    self.assertGreater(len(pair.variant), len(pair.baseline))
                elif pair.kind == "omission":
                    self.assertEqual(after, before[:2] + before[3:])
                    self.assertNotIn(pair.payload.materials, pair.variant)
                else:
                    self.assertEqual(after[:-1], before[:-1])
                    self.assertNotEqual(after[-1], before[-1])
