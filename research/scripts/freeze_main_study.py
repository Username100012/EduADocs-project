"""Freeze/check the reviewed main configuration locally; never calls an LLM."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from experiment.main_protocol import ARTIFACTS,canonical_hash,verify_frozen
from experiment.pilot_runner import build_plan


def freeze(path):
    if path.with_suffix(path.suffix+'.sha256').exists():
        raise ValueError('protocol already sealed; use --check, or a new protocol version for changes')
    config=json.loads(path.read_text(encoding='utf-8'))
    if config['status']!='ready_for_collection' or config['readiness_requirements']:
        raise ValueError('review is not complete')
    if len(config['tasks'])!=12 or any(not t.get('scope_review') for t in config['tasks']):
        raise ValueError('task scope review missing')
    jobs=build_plan(config)
    original=json.loads((ROOT/'artifacts/judge-contract-v2-preparation/preparation_report.json').read_text(encoding='utf-8'))['configuration_snapshot']
    if build_plan(original)!=jobs:
        raise ValueError('task review changed the original generation prompts or plan')
    preflight=json.loads((ROOT/'artifacts/gemini-main-preflight-after-credit.json').read_text(encoding='utf-8'))
    if preflight.get('generation',{}).get('model_version')!=config['generators']['gemini']['model'] or preflight['generation']['text'].strip()!='OK':
        raise ValueError('Gemini preflight does not match selected model')
    diagnosis=json.loads((ROOT/'artifacts/reserved-requirement-v2/relations_report.json').read_text(encoding='utf-8'))
    if diagnosis['completed']!=18 or diagnosis['statuses']!={'success':18}:
        raise ValueError('bounded diagnostic is incomplete')
    if config['judge']['configuration']!=original['judge']['configuration']:
        raise ValueError('judge parameters changed after diagnostics')
    for name,expected in config['judge']['contract']['artifact_sha256'].items():
        if sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('closed judge contract changed')
    config['freeze']={'frozen_on':'2026-10-25','kind':'local pre-main-collection freeze informed by pilot; not external preregistration',
        'catalog_sha256':canonical_hash(config['tasks']),'prompt_plan_sha256':canonical_hash(jobs),
        'artifact_sha256':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in ARTIFACTS},
        'change_policy':'Do not reseal the same protocol after collection. Any defining change requires a new version and separate output; preserve the original.'}
    path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    digest=sha256(path.read_bytes()).hexdigest()
    path.with_suffix(path.suffix+'.sha256').write_text(digest+'  '+path.name+'\n',encoding='utf-8')
    verify_frozen(path)
    return config


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    args=parser.parse_args()
    path=ROOT/'experiments/main_config.json'
    config=freeze(path) if args.freeze else verify_frozen(path)
    print(json.dumps({'protocol_version':config['protocol_version'],'status':config['status'],
        'tasks':len(config['tasks']),'planned_generations':len(build_plan(config)),
        'planned_judgments':config['judge']['planned_judgments_if_all_generations_succeed'],
        'config_file_sha256':sha256(path.read_bytes()).hexdigest(),'api_calls':0}))
