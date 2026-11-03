"""One frozen diagnostic round on new synthetic cases, separate from the pilot."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from experiment.judge_contract_v2 import build_prompt, response_schema
from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.pilot_runner import _hash
from check_openai_judge import request_body, read_key
from run_requirement_judgments import execute


def definition():
    payload = {'topic': 'Fila FIFO e ordem de atendimento', 'grade_level': 'Ensino superior introdutório em Computação',
        'learning_objectives': 'Simular inserção e remoção em uma fila FIFO e identificar a ordem de atendimento',
        'duration_minutes': 50, 'methodology': 'Resolução colaborativa de problemas',
        'materials': 'Cartões numerados e quadro',
        'assessment_strategy': 'Simular uma sequência de inserções e remoções e justificar a ordem FIFO'}
    lines = ['Tema: Fila FIFO e ordem de atendimento.', 'Nível: Ensino superior introdutório em Computação.',
        'Objetivos: Simular inserção e remoção em uma fila FIFO e identificar a ordem de atendimento.',
        'Duração total: 50 minutos.', 'Materiais: Cartões numerados e quadro.',
        'Metodologia: Resolução colaborativa de problemas. Em duplas, os estudantes ordenam cartões por chegada, inserem ao final da fila e removem do início, registrando cada estado no quadro.',
        'Etapas: apresentação do problema (10 minutos), simulação em duplas (25 minutos), avaliação (15 minutos).',
        'Avaliação: Simular uma sequência de inserções e remoções e justificar a ordem FIFO. Cada dupla registra a fila após cada operação; a justificativa deve indicar que o primeiro a entrar é o primeiro a sair.']
    base = '\n'.join(lines)
    omitted = '\n'.join(line for line in lines if not line.startswith('Materiais:'))
    # Remove all resource mentions, not just the labeled field.
    omitted = omitted.replace('cartões', 'elementos').replace('no quadro', 'na sequência')
    misaligned = '\n'.join(lines[:-1] + ['Avaliação: Listar capitais de países. A nota depende somente da grafia das capitais, sem considerar filas ou operações FIFO.'])
    cases = {'base': base, 'formatting': '\n'.join('**'+line.split(':',1)[0]+':**'+line.split(':',1)[1] for line in lines),
        'verbosity': base + '\nReforço: os estudantes retomam a explicação já apresentada e repetem a mesma sequência; este trecho apenas repete as instruções, sem adicionar recursos, etapas ou objetivos.',
        'omission': omitted, 'misalignment': misaligned,
        'duration_contradiction': base.replace('avaliação (15 minutos)', 'avaliação (35 minutos)')}
    return {'version': 'reserved-requirement-diagnostic-v1', 'repetitions': 3, 'payload': payload, 'cases': cases,
        'expected_relations': {'base': {'all_requirements': 'supported'},
            'formatting': {'same_as': 'base'}, 'verbosity': {'same_as': 'base'},
            'omission': {'materials': 'not_addressed'}, 'misalignment': {'assessment_strategy': 'contradicted'},
            'duration_contradiction': {'duration_minutes': 'contradicted'}},
        'scope': 'Authorial synthetic software/behavior diagnostic; one new topic, no human validation, no accuracy/general reliability claim.',
        'decision_policy': 'One round, no tuning or repeated collection. Report every mismatch. Any technical failure blocks pilot continuation. Semantic mismatches restrict conclusions and are not repaired by changing the rubric.'}


def prepare(directory):
    config = json.loads((ROOT / 'experiments/main_config.json').read_text(encoding='utf-8'))
    for name, expected in config['judge']['contract']['artifact_sha256'].items():
        if sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError('closed contract changed')
    spec = definition()
    manifest = {'definition': spec, 'definition_hash': _hash(spec), 'configuration_hash': _hash(config),
                'configuration': config['judge']['configuration'], 'contract': config['judge']['contract']}
    directory.mkdir(parents=True, exist_ok=True)
    seal = directory / 'reserved_manifest.json'
    if seal.exists():
        previous = json.loads(seal.read_text(encoding='utf-8'))
        if any(previous[k] != manifest[k] for k in ('definition', 'definition_hash', 'configuration', 'contract')):
            raise ValueError('reserved cases or configuration changed')
        manifest = previous
    else:
        seal.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return manifest


def load(source, directory):
    manifest = prepare(directory)
    spec = manifest['definition']
    payload = LessonPlanSemanticPayload.model_validate(spec['payload'])
    queue, mapping = [], {}
    for case, candidate in spec['cases'].items():
        for rep in range(1, 4):
            eid = 'eval-' + _hash([manifest['definition_hash'], manifest['configuration_hash'], case, rep])[:32]
            prompt = build_prompt(eid, payload, candidate)
            queue.append({'evaluation_id': eid, 'prompt': prompt.text, 'prompt_sha256': prompt.sha256,
                          'body': request_body(manifest['configuration'], prompt.text, response_schema())})
            mapping[eid] = {'job_id': case, 'repetition': rep}
    queue.sort(key=lambda row: row['evaluation_id'])
    plan = {'event': 'plan', 'protocol': spec['version'], 'planned': len(queue), 'automatic_retries': 0,
            'manifest_hash': _hash(manifest), 'requests_hash': _hash(queue)}
    return plan, queue, mapping, spec['cases']


def report(directory):
    spec = json.loads((directory / 'reserved_manifest.json').read_text(encoding='utf-8'))['definition']
    summary = json.loads((directory / 'summary.v2.json').read_text(encoding='utf-8'))
    rows = {r['job_id']: r for r in summary['responses']}
    checks = []
    for name, expected in spec['expected_relations'].items():
        row = rows.get(name)
        if not row or not row['complete_triplet']:
            checks.append({'case': name, 'relation': expected, 'result': 'incomplete'})
            continue
        if 'same_as' in expected:
            base = rows.get(expected['same_as'])
            if not base or not base['complete_triplet']:
                result = 'incomplete'
            else:
                result = 'satisfied' if all(row['requirements'][k]['frequencies'] == base['requirements'][k]['frequencies'] for k in row['requirements']) else 'violated'
        elif 'all_requirements' in expected:
            result = 'satisfied' if all(r['frequencies'] == {expected['all_requirements']: 3} for r in row['requirements'].values()) else 'violated'
        else:
            result = 'satisfied' if all(row['requirements'][k]['frequencies'] == {value: 3} for k,value in expected.items()) else 'violated'
        checks.append({'case': name, 'relation': expected, 'result': result})
    out = {'planned_judgments': 18, 'completed': summary['completed'], 'statuses': summary['statuses'],
           'checks': checks, 'check_counts': dict(Counter(c['result'] for c in checks)),
           'scope': spec['scope'], 'decision_policy': spec['decision_policy']}
    (directory / 'relations_report.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'artifacts/reserved-requirement-v2')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    manifest = prepare(args.output)
    if args.live:
        key = read_key()
        if not key:
            raise SystemExit('credential absent')
        execute(args.output, args.output, key, max_jobs=18, workers=args.workers, plan_loader=load)
        print(json.dumps(report(args.output)))
    else:
        print(json.dumps({'planned': 18, 'api_calls': 0, 'definition_hash': manifest['definition_hash']}))
