"""Audit verifies provenance and reports extraction limits without revising scores."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.automatic_metrics import evaluate_text


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit_module = load_script("audit_pilot_metrics")
evaluate_module = load_script("evaluate_pilot")


class PilotMetricsAuditTests(unittest.TestCase):
    def test_formatting_failure_is_flagged_without_replacing_baseline(self):
        task = json.loads((ROOT / "experiments/pilot_config.json").read_text(encoding="utf-8"))["tasks"][0]
        text = "**3. Recursos e Materiais**\n- Quadro e folha\n"
        baseline = evaluate_text(text, task)["requirements"]["materials"]
        result = audit_module.audit_cell(text, task, "materials", baseline)
        self.assertEqual(result["baseline_state"], "undetermined")
        self.assertTrue(result["diagnostic_whole_text"]["present"])
        self.assertIn("lexical_evidence_outside_recognized_section", [f["type"] for f in result["flags"]])
        self.assertIsNone(baseline["present"])

    def test_duration_multiplier_is_flagged_not_silently_corrected(self):
        task = {"payload": {"duration_minutes": 50}}
        from experiment.automatic_metrics import duration_metrics
        text = "Duração: 2 aulas (90 minutos cada)"
        baseline = duration_metrics(text, 50)
        result = audit_module.audit_cell(text, task, "duration_minutes", baseline)
        self.assertEqual(baseline["declared"][0]["minutes"], 90)
        self.assertIn("multiple_lessons_not_multiplied", [f["type"] for f in result["flags"]])

    def test_complete_saved_pilot_is_reproducible_and_inputs_unchanged(self):
        source = ROOT / "artifacts/pilot-qwen3-local"
        if not (source / "generations.jsonl").exists():
            self.skipTest("saved pilot absent")
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for name in ("generations.jsonl", "automatic_metrics.json"):
                (directory / name).write_bytes((source / name).read_bytes())
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            report = audit_module.audit(directory)
            self.assertEqual(len(report["cells"]), 189)
            self.assertEqual(len(report["by_task_condition"]), 63)
            self.assertTrue(report["recomputed_metrics_match"])
            self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})
            metrics = json.loads((directory / "automatic_metrics.json").read_text(encoding="utf-8"))
            metrics["source_log_sha256"] = "bad"
            (directory / "automatic_metrics.json").write_text(json.dumps(metrics))
            with self.assertRaisesRegex(ValueError, "different source log"):
                audit_module.audit(directory)
