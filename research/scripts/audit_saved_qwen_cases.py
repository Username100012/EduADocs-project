"""Post-hoc local case audit; does not replace frozen measures or call APIs."""
import json
import re
from collections import Counter
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/main-judgments-v1/case-audit'
TIME = re.compile(r'\((\d+)\s*minutos?\)', re.I)
INTERVAL = re.compile(r'^\|\s*(\d+)\s*[–−-]\s*(\d+)\s*(?:min(?:utos?)?)\s*\|', re.I)


def inspect_schedule(text):
    numbered = []
    intervals = []
    for n, line in enumerate(text.splitlines(), 1):
        interval = INTERVAL.search(line)
        if interval:
            a, b = map(int, interval.groups())
            intervals.append({'line': n, 'quote': line, 'start': a, 'end': b,
                              'duration': b-a,
                              'embedded_minutes': [int(x) for x in TIME.findall(line)]})
        match = TIME.search(line)
        if match and not line.lstrip().startswith(('|', '-', '* ')):
            clean = line.lstrip('# ').replace('**', '')
            if re.match(r'(?:[IVXLCDM]+\.|\d+(?:\.\d+)*\.|[A-Z]\.|Etapa\s+\d+\s*:)', clean) or line.startswith(('#','**')):
                numbered.append({'line': n, 'quote': line, 'minutes': int(match[1]),
                                 'level': len(line)-len(line.lstrip('#')),
                                 'optional': 'opcional' in line.lower()})
    # Shallowest timed numbered headings only: never add parents and children.
    if numbered:
        markdown = [r for r in numbered if r['level'] > 0]
        pool = markdown or numbered
        level = min(r['level'] for r in pool)
        stages = [r for r in pool if r['level'] == level and not r['optional']]
    else:
        stages = []
    return {'scope': 'Exploratory syntactic extraction, not a new primary metric or adjudication.',
            'numbered_timed_headings': numbered, 'selected_top_level_stages': stages,
            'selected_stage_sum': sum(r['minutes'] for r in stages) if stages else None,
            'interval_rows': intervals,
            'intervals_contiguous': all(a['end'] == b['start'] for a,b in zip(intervals, intervals[1:])) if intervals else None,
            'interval_duration_sum': sum(r['duration'] for r in intervals) if intervals else None,
            'interval_label_mismatches': [r for r in intervals if any(v != r['duration'] for v in r['embedded_minutes'])]}


def main():
    directory = ROOT / 'artifacts/main-judgments-v1'
    gen_path = ROOT / 'artifacts/main-study-v1/generations.jsonl'
    log_path = directory / 'judgments.v2.jsonl'
    before = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in (gen_path, log_path)}
    generations = [json.loads(l) for l in gen_path.read_text(encoding='utf-8').splitlines()]
    jobs = {j['job_id']: j for j in generations[0]['jobs']}
    mapping = {r['evaluation_id']: r for r in map(json.loads, (directory/'mapping.jsonl').read_text(encoding='utf-8').splitlines())}
    results = [r for r in map(json.loads, log_path.read_text(encoding='utf-8').splitlines()) if r.get('event') == 'result']
    OUT.mkdir(exist_ok=True)
    cases = []
    for generation in generations:
        if generation.get('status') != 'success':
            continue
        job = jobs[generation['job_id']]
        if job['generator_id'] != 'qwen3' or job['condition'] not in ('c1','c2'):
            continue
        jid = job['job_id']
        text = generation['response']['content']
        filename = jid.replace(':','_') + '.md'
        # Verbatim LF-numbered excerpts are kept separate from the raw collection.
        (OUT/filename).write_text('\n'.join(f'{i:03}: {s}' for i,s in enumerate(text.splitlines(),1))+'\n', encoding='utf-8')
        selected = [e for e in results if mapping[e['evaluation_id']]['job_id'] == jid]
        assert len(selected) == 3
        requirements = ['duration_minutes']
        if job['task_id'] in ('task-007','task-012'):
            requirements.append('learning_objectives')
        cases.append({'job_id': jid, 'task_id': job['task_id'], 'condition': job['condition'],
            'candidate_sha256': sha256(text.encode()).hexdigest(),
            'expected_duration_minutes': job['payload']['duration_minutes'],
            'expected_learning_objectives': job['payload']['learning_objectives'],
            'numbered_source': filename, 'schedule_diagnostic': inspect_schedule(text),
            'judgments': [{'evaluation_id': e['evaluation_id'], 'repetition': mapping[e['evaluation_id']]['repetition'],
                'execution_status': e['status'],
                'requirements': {k:e['validated']['requirements'][k] for k in requirements} if e['status']=='success' else None,
                'secondary_assessments': e['validated']['assessments'] if e['status']=='success' else None,
                'error': e.get('error')} for e in selected]})
    assert len(cases) == 72
    assert sum(c['task_id'] in ('task-007', 'task-012') for c in cases) == 12
    assert all(sha256((ROOT/name).read_bytes()).hexdigest()==value for name,value in before.items())
    audit = {'audit_type':'post-hoc exploratory computational case audit, not a new collection or human evaluation',
             'api_calls':0, 'primary_classifications_changed':False, 'raw_hashes':before,
             'duration_plans':72, 'objective_plans':12, 'cases':sorted(cases,key=lambda c:c['job_id'])}
    (OUT/'cases.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for c in audit['cases']:
        d=c['schedule_diagnostic']
        frequencies=Counter(j['requirements']['duration_minutes']['status'] for j in c['judgments'] if j['requirements'])
        print(c['job_id'],d['selected_stage_sum'],d['interval_duration_sum'],len(d['interval_label_mismatches']),dict(frequencies))


if __name__ == '__main__':
    main()
