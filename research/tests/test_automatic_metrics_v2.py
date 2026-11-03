"""Synthetic invariance and negative controls; no pilot texts used as fixtures."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from experiment import automatic_metrics as v1
from experiment import automatic_metrics_v2 as v2

TASK = {'payload': {'duration_minutes': 40}, 'textual_evidence': {
    'topic_concept_groups': [['grafos']], 'grade_aliases': ['graduação'],
    'objective_verbs': ['representar'], 'methodology_aliases': ['aprendizagem por projetos'],
    'required_resource_groups': [['papel'], ['lápis']],
    'assessment_action_groups': [['desenhar'], ['grafo']]}}
FIELDS = [('Nível', 'Graduação'), ('Duração da aula', '40 minutos'),
          ('Objetivos de Aprendizagem', 'Representar grafos.'),
          ('Metodologia', 'Aprendizagem por projetos.'),
          ('Recursos e Materiais', 'Papel e lápis.'),
          ('Avaliação', 'Desenhar um grafo.')]


def states(text):
    r = v2.evaluate_text(text, TASK)['requirements']
    return {k: v['present'] if k != 'duration_minutes' else v['declared_matches_target'] for k, v in r.items()}


class MetricsV2Tests(unittest.TestCase):
    def test_seven_requirements_invariant_to_supported_formatting(self):
        variants = [
            '\n'.join(f'{k}: {v}' for k, v in FIELDS),
            '\n'.join(f'- **{k}:** {v}' for k, v in FIELDS),
            '\n'.join(f'### {i}. **{k}**\n{v}' for i, (k, v) in enumerate(FIELDS, 1)),
            '\n'.join(f'**{i}. {k}**\n- {v}' for i, (k, v) in enumerate(FIELDS, 1)),
            '\n\n'.join(f'## {i}.1 {k}:\n\n{v}' for i, (k, v) in enumerate(FIELDS, 1)),
        ]
        expected = {key: True for key in states(variants[0])}
        for text in variants:
            with self.subTest(text=text):
                self.assertEqual(states(text), expected)
        evidence = v2.evaluate_text(variants[1], TASK)['requirements']['materials']['groups'][0]['evidence'][0]
        self.assertEqual(evidence['line'], 5)
        self.assertEqual(evidence['text'], '- **Recursos e Materiais:** Papel e lápis.')

    def test_markdown_inside_lexical_expression(self):
        self.assertTrue(v2.group_presence(v2.lines_with_sections('Objetivos:\nRepresentar **grafos**.'), [['grafos']], section='objective')['present'])

    def test_scope_does_not_leak_into_other_section_or_metadata(self):
        for boundary in ('## Referências', '**2. Referências**', 'Referências:', '- Nível: Graduação'):
            text = 'Objetivos:\nLer o texto.\n' + boundary + '\nRepresentar grafos.'
            with self.subTest(boundary=boundary):
                self.assertFalse(states(text)['learning_objectives'])
        self.assertIsNone(states('Representar grafos.\nMateriais:\nPapel e lápis.')['learning_objectives'])

    def test_unknown_headings_remain_unknown(self):
        self.assertIsNone(states('Insumos:\nPapel e lápis.')['materials'])

    def test_negation_and_domain_nonfunctional_category(self):
        self.assertIsNone(v2.group_presence(v2.lines_with_sections('Não usar papel'), [['papel']])['present'])
        lines = v2.lines_with_sections('Especificar requisitos não funcionais da biblioteca.')
        self.assertTrue(v2.group_presence(lines, [['não funcionais'], ['biblioteca']])['present'])
        self.assertFalse(v2.group_presence(lines, [['funcionais']])['present'])
        self.assertIsNone(v2.group_presence(v2.lines_with_sections('Não especificar requisitos não funcionais da biblioteca.'), [['biblioteca']])['present'])

    def test_duration_labels_units_and_multiplied_lessons(self):
        for text in ('Duração: 2 aulas (45 minutos cada)', '- **Carga horária:** 1 hora e 30 minutos', '### 2. Duração da aula\n90 minutos'):
            with self.subTest(text=text):
                self.assertTrue(v2.duration_metrics(text, 90)['declared_matches_target'])
        self.assertIsNone(v2.duration_metrics('Duração: 2 aulas (90 minutos)', 90)['declared_matches_target'])
        self.assertIsNone(v2.duration_metrics('Atividade: 90 minutos', 90)['declared_matches_target'])

    def test_target_mismatch_is_separate_from_internal_inconsistency(self):
        r = v2.duration_metrics('Duração: 60 minutos', 40)
        self.assertTrue(r['target_mismatch_detected'])
        self.assertIsNone(r['internal_inconsistency_detected'])

    def test_next_metadata_is_not_a_duration_value(self):
        r = v2.duration_metrics('Duração:\nMetodologia: debate de 40 minutos', 40)
        self.assertIsNone(r['declared_matches_target'])
        self.assertEqual(len(r['unresolved_declarations']), 1)

    def test_positive_and_negative_occurrences_keep_separate_evidence(self):
        r = v2.group_presence(v2.lines_with_sections('Não usar papel; usar papel.'), [['papel']])
        # Negation scope remains deliberately conservative on a shared line.
        self.assertIsNone(r['present'])
        r = v2.group_presence(v2.lines_with_sections('Não usar papel.\nUsar papel.'), [['papel']])
        self.assertTrue(r['present'])
        self.assertEqual([e['ambiguous_context'] for e in r['groups'][0]['evidence']], [True, False])

    def test_internal_duration_conflict_and_unknown_schedule(self):
        r = v2.duration_metrics('Duração: 40 minutos\n00:00–00:20\n00:20–01:00', 40)
        self.assertTrue(r['internal_inconsistency_detected'])
        self.assertTrue(r['target_mismatch_detected'])
        self.assertIsNone(v2.duration_metrics('00:00–00:30\n00:20–00:40', 40)['clock_schedule_minutes'])
        r = v2.duration_metrics('Nada declarado', 40)
        self.assertIsNone(r['target_mismatch_detected'])
        self.assertIsNone(r['internal_inconsistency_detected'])

    def test_mixed_levels_are_flagged_without_semantic_claim(self):
        r = v2.evaluate_text('Graduação ou ensino médio.', TASK)['requirements']['grade_level']
        self.assertTrue(r['present'])
        self.assertTrue(r['mixed_school_levels_mentioned'])

    def test_empty_and_version_separation(self):
        self.assertIsNone(v2.evaluate_text('', {})['requirements'])
        self.assertEqual(v1.METRICS_VERSION, 'eduadocs-textual-proxies-v1')
        self.assertNotEqual(v1.METRICS_VERSION, v2.METRICS_VERSION)
        self.assertIsNone(v1.duration_metrics('Duração da aula: 40 minutos', 40)['declared_matches_target'])
