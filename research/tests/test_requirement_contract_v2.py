"""Offline contract checks do not claim semantic validity of fixture labels."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.judge_contract_v2 import (build_prompt, parse_response, response_schema, ContractError,
    SCHEMA_VERSION, RUBRIC_VERSION, CRITERIA)
from experiment.requirement_measurement import observe_requirements
from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.prompt_conditions import EXPERIMENTAL_REQUIREMENTS

EID = 'eval-' + 'a' * 32
CANDIDATE = 'Tópico: Grafos\nMateriais: papel e lápis\nAtividade e avaliação: desenhar um grafo.'


def fixture():
    # A syntactic fixture. supported labels are not a semantic reference.
    evidence = [{'line_start': 1, 'line_end': 1, 'quote': CANDIDATE.splitlines()[0]}]
    return {'schema_version': SCHEMA_VERSION, 'rubric_version': RUBRIC_VERSION,
            'evaluation_id': EID, 'requirements': {k: {'status': 'uncertain', 'evidence': [],
            'justification': 'Fixture sem avaliação semântica.'} for k in EXPERIMENTAL_REQUIREMENTS},
            'assessments': {k: {'score': 1, 'evidence': evidence, 'justification': 'Fixture.'} for k in CRITERIA}}


class RequirementContractTests(unittest.TestCase):
    def assert_code(self, data, code):
        with self.assertRaises(ContractError) as ctx:
            parse_response(json.dumps(data), EID, CANDIDATE)
        self.assertEqual(ctx.exception.code, code)

    def test_every_state_is_nominal_and_validated_locally(self):
        for state in ('supported', 'partial', 'not_addressed', 'contradicted', 'uncertain'):
            data = fixture()
            row = data['requirements']['materials']
            row['status'] = state
            if state in {'supported', 'partial', 'contradicted'}:
                row['evidence'] = [{'line_start': 2, 'line_end': 2, 'quote': CANDIDATE.splitlines()[1]}]
            parsed = parse_response(json.dumps(data), EID, CANDIDATE)
            self.assertEqual(parsed.requirements.materials.status, state)

    def test_missing_or_extra_requirement_and_old_version_are_rejected(self):
        data = fixture(); del data['requirements']['materials']; self.assert_code(data, 'schema_error')
        data = fixture(); data['requirements']['extra'] = data['requirements']['topic']; self.assert_code(data, 'schema_error')
        data = fixture(); data['schema_version'] = 'old'; self.assert_code(data, 'schema_error')

    def test_duplicate_keys_nonfinite_json_and_wrong_id_are_rejected(self):
        for raw, code in [('{"a":1,"a":2}', 'duplicate_key'), ('{"a":NaN}', 'invalid_json'), ('[]', 'non_object_root'), ('', 'empty_response')]:
            with self.assertRaises(ContractError) as ctx:
                parse_response(raw, EID, CANDIDATE)
            self.assertEqual(ctx.exception.code, code)
        data = fixture(); data['evaluation_id'] = 'eval-' + 'b'*32
        self.assert_code(data, 'evaluation_id_mismatch')

    def test_fabricated_or_out_of_range_citations_are_rejected(self):
        for evidence in ({'line_start': 2, 'line_end': 2, 'quote': 'inventado'},
                         {'line_start': 4, 'line_end': 4, 'quote': 'fora'},
                         {'line_start': 2, 'line_end': 1, 'quote': 'ordem'}):
            data = fixture(); data['requirements']['materials'].update(status='supported', evidence=[evidence])
            self.assert_code(data, 'evidence_mismatch')

    def test_empty_evidence_and_blank_justifications_are_not_repaired(self):
        data = fixture(); data['requirements']['materials']['status'] = 'supported'
        self.assert_code(data, 'evidence_status_inconsistent')
        data = fixture(); data['requirements']['materials']['status'] = 'not_addressed'
        data['requirements']['materials']['evidence'] = [{'line_start': 1, 'line_end': 1, 'quote': CANDIDATE.splitlines()[0]}]
        self.assert_code(data, 'evidence_status_inconsistent')
        data = fixture(); data['requirements']['materials']['justification'] = ' '
        self.assert_code(data, 'blank_justification')

    def test_float_boolean_scores_and_missing_criterion_evidence(self):
        for value in (True, 4.0, '4'):
            data = fixture(); data['assessments']['instructional_alignment']['score'] = value
            with self.assertRaises(ContractError):
                parse_response(json.dumps(data), EID, CANDIDATE)
        data = fixture(); data['assessments']['instructional_alignment'].update(score=3, evidence=[])
        self.assert_code(data, 'evidence_status_inconsistent')

    def test_multiline_quotes_and_numbered_candidate_binding(self):
        data = fixture()
        data['requirements']['materials'].update(status='partial', evidence=[{'line_start': 1, 'line_end': 2,
            'quote': '\n'.join(CANDIDATE.splitlines()[:2])}])
        parse_response(json.dumps(data), EID, CANDIDATE)
        payload = LessonPlanSemanticPayload(topic='Grafos', grade_level='Graduação', learning_objectives='Representar grafos',
            duration_minutes=40, methodology='Discussão', materials='Papel', assessment_strategy='Desenhar grafos')
        prompt = build_prompt(EID, payload, CANDIDATE)
        self.assertEqual(prompt.semantic_payload_hash, payload.semantic_hash)
        self.assertIn('"line": 2, "text": "Materiais: papel e lápis"', prompt.text)
        self.assertNotIn('semantic_fidelity', CRITERIA)

    def test_all_literal_targets_have_observable_fields_without_alias_tuning(self):
        config = json.loads((ROOT/'experiments/main_config.json').read_text(encoding='utf-8'))
        labels = ('Tópico', 'Nível', 'Objetivos', 'Duração', 'Metodologia', 'Materiais', 'Avaliação')
        for task in config['tasks']:
            payload = task['payload']
            for variant in ('plain', 'markdown'):
                lines = []
                for i, (label, key) in enumerate(zip(labels, EXPERIMENTAL_REQUIREMENTS), 1):
                    value = str(payload[key]) + (' minutos' if key == 'duration_minutes' else '')
                    lines.append(f'{label}: {value}' if variant == 'plain' else f'### {i}. **{label}**\n{value}')
                result = observe_requirements('\n'.join(lines), 50)
                self.assertEqual({r['observation'] for r in result['fields'].values()}, {'detected'})

    def test_negated_or_missing_materials_are_structural_observations_not_semantic_labels(self):
        result = observe_requirements('Materiais: Não utilizar quadro.', 50)
        self.assertEqual(result['fields']['materials']['observation'], 'detected')
        self.assertEqual(observe_requirements('Materiais:\n## Referências\nPapel.', 50)['fields']['materials']['observation'], 'empty')
        self.assertEqual(observe_requirements('Conteúdo sem rótulo.', 50)['fields']['materials']['observation'], 'not_detected')
