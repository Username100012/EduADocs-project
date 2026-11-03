"""Offline consolidation keeps original data and links each blinded judge prompt."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("summarize_local_pilot", ROOT / "scripts/summarize_local_pilot.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LocalSummaryTests(unittest.TestCase):
    def test_saved_run_consolidation_and_blinded_queue_are_reproducible(self):
        source = ROOT / "artifacts/pilot-qwen3-local"
        if not (source / "automatic_metrics.v2.json").exists():
            self.skipTest("saved pilot not available")
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            names = ("generations.jsonl", "automatic_metrics.json", "automatic_metrics.v2.json")
            originals = {name: (source / name).read_bytes() for name in names}
            for name, data in originals.items():
                (directory / name).write_bytes(data)
            report = module.consolidate(directory)
            self.assertEqual(report["total_cells"], 189)
            self.assertEqual(len(report["by_task_condition"]), 63)
            self.assertEqual(report["semantic_judgments_executed"], 0)
            self.assertEqual(originals, {name: (directory / name).read_bytes() for name in names})
            queue = [json.loads(line) for line in (directory / "judge_queue.jsonl").read_text(encoding="utf-8").splitlines()]
            mapping = [json.loads(line) for line in (directory / "judge_mapping.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(queue), 81)
            self.assertEqual(len({r["evaluation_id"] for r in queue}), 81)
            self.assertEqual({r["evaluation_id"] for r in queue}, {r["evaluation_id"] for r in mapping})
            for row in queue:
                self.assertEqual(set(row), {"evaluation_id", "prompt", "prompt_sha256", "prompt_version"})
                self.assertEqual(sha256(row["prompt"].encode()).hexdigest(), row["prompt_sha256"])
                self.assertNotRegex(row["prompt"], r"qwen3:pilot-|gemini:pilot-")
            outputs = {p.name: p.read_bytes() for p in directory.iterdir()}
            module.consolidate(directory)
            self.assertEqual(outputs, {p.name: p.read_bytes() for p in directory.iterdir()})
            data = json.loads((directory / "automatic_metrics.v2.json").read_text(encoding="utf-8"))
            data["records"][0]["metrics"]["word_count"] += 1
            (directory / "automatic_metrics.v2.json").write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "stale"):
                module.consolidate(directory)
