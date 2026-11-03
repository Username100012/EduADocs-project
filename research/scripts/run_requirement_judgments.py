"""Execute the sealed v2 queue; dry run by default, no automatic retries."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
import tempfile
from time import perf_counter

from filelock import FileLock
import requests
from prepare_requirement_judgments import prepare
from check_openai_judge import read_key, redact
from experiment.judge_contract_v2 import parse_response, ContractError
from experiment.pilot_runner import _append


def load(source, directory):
    # Rebuild independently: checks source logs, contract hashes, configuration,
    # all prompts, request bodies and mapping before permitting a paid call.
    with tempfile.TemporaryDirectory() as temporary:
        check = Path(temporary)
        stored = json.loads((directory / 'preparation_report.json').read_text(encoding='utf-8'))
        report = prepare(source, check, configuration=stored.get('configuration_snapshot'))
        for name in ('queue.jsonl', 'mapping.jsonl', 'preparation_report.json'):
            expected = (check / name).read_text(encoding='utf-8')
            actual = (directory / name).read_text(encoding='utf-8')
            if name.endswith('.jsonl'):
                same = list(map(json.loads, expected.splitlines())) == list(map(json.loads, actual.splitlines()))
            else:
                same = json.loads(expected) == json.loads(actual)
            if not same:
                raise ValueError('queue provenance mismatch: ' + name)
    if report['simulated_generations']:
        raise ValueError('simulated sources cannot enter real judgments')
    queue = [json.loads(s) for s in (directory / 'queue.jsonl').read_text(encoding='utf-8').splitlines()]
    mapping = {r['evaluation_id']: r for r in map(json.loads, (directory / 'mapping.jsonl').read_text(encoding='utf-8').splitlines())}
    events = list(map(json.loads, (source / 'generations.jsonl').read_text(encoding='utf-8').splitlines()))
    candidates = {e['job_id']: e['response']['content'] for e in events[1:] if e['event'] == 'result' and e['status'] == 'success'}
    plan = {'event': 'plan', 'protocol': 'requirement-judgments-v2', 'planned': len(queue),
            'automatic_retries': 0, 'source_log_sha256': report['source_log_sha256'],
            'configuration_hash': report['configuration_hash'], 'contract': report['contract'],
            'queue_sha256': sha256((directory / 'queue.jsonl').read_bytes()).hexdigest()}
    if events[0]['config'].get('study_phase') == 'main':
        from experiment.main_protocol import verify_frozen
        active_path = Path(__file__).resolve().parents[1] / 'experiments/main_config.json'
        active = verify_frozen(active_path)
        if active != events[0]['config']:
            raise ValueError('main source differs from frozen configuration')
        plan['execution_policy'] = active['judge']['execution_policy']
    return plan, queue, mapping, candidates


def summarize(events, mapping):
    groups = defaultdict(list)
    for event in events:
        if event.get('event') == 'result':
            groups[mapping[event['evaluation_id']]['job_id']].append(event)
    rows = []
    for job, attempts in sorted(groups.items()):
        valid = [e['validated'] for e in attempts if e['status'] == 'success']
        complete = len(attempts) == 3 and len(valid) == 3
        requirements = {name: {'frequencies': dict(Counter(v['requirements'][name]['status'] for v in valid)),
                               'exact_agreement': len({v['requirements'][name]['status'] for v in valid}) == 1 if complete else None}
                        for name in (valid[0]['requirements'] if valid else [])}
        assessments = {name: {'scores': [v['assessments'][name]['score'] for v in valid],
                               'median': median(v['assessments'][name]['score'] for v in valid) if complete else None}
                       for name in (valid[0]['assessments'] if valid else [])}
        rows.append({'job_id': job, 'valid': len(valid), 'complete_triplet': complete,
                     'requirements': requirements, 'assessments': assessments})
    results = [e for e in events if e.get('event') == 'result']
    return {'protocol': 'requirement-judgments-v2', 'completed': len(results),
            'statuses': dict(Counter(e['status'] for e in results)), 'responses': rows,
            'interpretation': 'Nominal frequencies, not a composite score. Incomplete triplets have no median or agreement.'}


def execute(source, directory, key, *, max_jobs, post=None, workers=1, plan_loader=None, continue_validation_errors=False):
    if not 1 <= workers <= 8:
        raise ValueError('workers must be between 1 and 8')
    if max_jobs <= 0:
        raise ValueError('max_jobs must be positive')
    plan, queue, mapping, candidates = (plan_loader or load)(source, directory)
    policy = plan.get('execution_policy')
    if policy and (workers != policy['workers'] or continue_validation_errors != policy['continue_validation_errors']):
        raise ValueError('judge execution parameters differ from frozen policy')
    path = directory / 'judgments.v2.jsonl'
    post = post or requests.post
    with FileLock(str(path) + '.lock', timeout=0):
        events = []
        if path.exists():
            raw = path.read_text(encoding='utf-8')
            if not raw.endswith('\n'):
                raise ValueError('incomplete log')
            events = list(map(json.loads, raw.splitlines()))
            if events[0] != plan:
                raise ValueError('execution plan changed')
        started, finished = set(), set()
        allowed = set(mapping)
        for e in events[1:]:
            eid = e['evaluation_id']
            if eid not in allowed:
                raise ValueError('unknown evaluation')
            if e['event'] == 'started' and eid not in started:
                started.add(eid)
            elif e['event'] == 'result' and eid in started and eid not in finished:
                finished.add(eid)
            else:
                raise ValueError('invalid event sequence')
        if started - finished:
            raise ValueError('unresolved started call; refusing duplicate')
        with path.open('a', encoding='utf-8', newline='\n') as stream:
            if not events:
                _append(stream, plan)
                events.append(plan)
            pending = [row for row in queue if row['evaluation_id'] not in finished][:max_jobs]
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for offset in range(0, len(pending), workers):
                    wave = pending[offset:offset + workers]
                    futures = []
                    for row in wave:
                        entry = {'event': 'started', 'evaluation_id': row['evaluation_id'],
                                 'workers': workers, 'continue_validation_errors': continue_validation_errors, 'at': datetime.now(timezone.utc).isoformat()}
                        _append(stream, entry)
                        events.append(entry)
                        futures.append(pool.submit(call_one, row, mapping, candidates, key, post))
                    failed = False
                    for future in as_completed(futures):
                        event = future.result()
                        _append(stream, event)
                        events.append(event)
                        failed |= event['status'] != 'success' and not (continue_validation_errors and event['status'] == 'validation_error')
                        print(json.dumps({'evaluation_id': event['evaluation_id'], 'status': event['status']}), flush=True)
                    # Drain already-started calls; never submit another wave after failure.
                    if failed:
                        break
        report = summarize(events, mapping)
        report['planned'] = len(queue)
        (directory / 'summary.v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return report




def call_one(row, mapping, candidates, key, post):
    eid = row['evaluation_id']
    event = {'event': 'result', 'evaluation_id': eid, 'status': 'transport_error',
             'validated': None, 'raw_response': None, 'raw_text': None, 'http_status': None}
    start = perf_counter()
    try:
        response = post('https://api.openai.com/v1/responses',
                        headers={'Authorization': 'Bearer ' + key}, json=row['body'], timeout=120)
        event['http_status'] = response.status_code
        event['request_id'] = response.headers.get('x-request-id')
        raw = response.json()
        event['raw_response'] = raw
        if not response.ok:
            event['status'] = 'api_error'
        elif raw.get('model') != row['body']['model']:
            event['status'] = 'model_mismatch'
        elif raw.get('status') != 'completed':
            event['status'] = 'incomplete_response'
        elif any(c.get('type') == 'refusal' for o in raw.get('output', []) for c in o.get('content', [])):
            event['status'] = 'refusal'
        else:
            text = ''.join(c['text'] for o in raw.get('output', []) for c in o.get('content', []) if c.get('type') == 'output_text')
            event['raw_text'] = text
            try:
                validated = parse_response(text, eid, candidates[mapping[eid]['job_id']])
                event.update(status='success', validated=validated.model_dump(mode='json'))
            except ContractError as error:
                event.update(status='validation_error', error={'code': error.code, 'path': error.path, 'message': str(error)})
    except (requests.RequestException, ValueError) as error:
        event['error'] = {'type': type(error).__name__}
    event.update(latency_ms=(perf_counter() - start) * 1000, at=datetime.now(timezone.utc).isoformat())
    event = redact(event, key)
    return event


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('queue', type=Path)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--max-jobs', type=int, default=1)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--continue-validation-errors', action='store_true')
    args = parser.parse_args()
    if args.live:
        key = read_key()
        if not key:
            raise SystemExit('OPENAI_API_KEY ausente')
        report = execute(args.source, args.queue, key, max_jobs=args.max_jobs, workers=args.workers, continue_validation_errors=args.continue_validation_errors)
        print(json.dumps({k: report[k] for k in ('completed', 'statuses', 'planned')}))
    else:
        plan, *_ = load(args.source, args.queue)
        print(json.dumps({'validated_plan': True, 'planned': plan['planned'], 'api_calls': 0}))
