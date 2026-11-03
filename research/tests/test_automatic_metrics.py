"""Boundary cases prevent lexical evidence being mistaken for semantic validity."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.automatic_metrics import duration_metrics, evaluate_text, group_presence, lines_with_sections


class AutomaticMetricsTests(unittest.TestCase):
    def test_declared_50_schedule_60(self):
        r = duration_metrics("**Duração:**\n50 minutos\n00:00 – 00:15\n00:15 – 01:00", 50)
        self.assertTrue(r["declared_matches_target"])
        self.assertEqual(r["clock_schedule_minutes"], 60)
        self.assertTrue(r["detected_contradiction"])

    def test_hours_minutes_and_unknown_duration(self):
        r = duration_metrics("Duração total: 1 hora e 30 minutos", 90)
        self.assertEqual(r["declared"][0]["minutes"], 90)
        self.assertTrue(r["declared_matches_target"])
        self.assertIsNone(duration_metrics("Atividade: 10 minutos", 50)["declared_matches_target"])

    def test_overlap_or_repeated_schedule_not_summed(self):
        r = duration_metrics("00:00-00:30\n00:20-00:50", 50)
        self.assertIsNone(r["clock_schedule_minutes"])

    def test_functional_is_not_matched_inside_nonfunctional(self):
        r = group_presence(lines_with_sections("Requisitos não funcionais"), [["funcionais"]])
        self.assertFalse(r["present"])

    def test_negation_is_not_counted_as_positive(self):
        r = group_presence(lines_with_sections("Não utilizar quadro"), [["quadro"]])
        self.assertIsNone(r["present"])

    def test_objective_word_elsewhere_is_not_objective_evidence(self):
        task = json.loads((ROOT / "experiments/pilot_config.json").read_text())["tasks"][0]
        r = evaluate_text("Implementar busca linear em vetores.\n**Materiais:**\nQuadro e folha.", task)
        self.assertIsNone(r["requirements"]["learning_objectives"]["present"])
        self.assertTrue(r["requirements"]["materials"]["present"])

    def test_objective_intro_sentence_does_not_end_section(self):
        lines = lines_with_sections("**Objetivo de Aprendizagem:**\nAo final da aula, os alunos serão capazes de:\n- Implementar busca linear.")
        self.assertTrue(group_presence(lines, [["implementar"]], section="objective")["present"])

    def test_qwen_saved_preflight_detects_real_contradiction(self):
        task = json.loads((ROOT / "experiments/pilot_config.json").read_text())["tasks"][0]
        path = ROOT / "artifacts/qwen3-preflight/plano_de_aula.md"
        if not path.exists():
            self.skipTest("optional local preflight artifact absent")
        r = evaluate_text(path.read_text(encoding="utf-8-sig"), task)
        self.assertEqual(len(r["requirements"]), 7)
        self.assertTrue(r["requirements"]["duration_minutes"]["detected_contradiction"])
        self.assertGreater(r["word_count"], 0)

    def test_empty_response_has_no_requirement_scores(self):
        r = evaluate_text("  ", {})
        self.assertIsNone(r["requirements"])
