"""Descriptive publication tables from saved v2 judgments; never call APIs."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
from run_requirement_judgments import load, summarize


def report(source, directory, recovery=None):
    plan, queue, mapping, candidates = load(source, directory)
    events = list(map(json.loads, (directory/'judgments.v2.jsonl').read_text(encoding='utf-8').splitlines()))
    if events[0] != plan:
        raise ValueError('source provenance mismatch')
    starts, results = set(), {}
    for event in events[1:]:
        eid=event['evaluation_id']
        if eid not in mapping:
            raise ValueError('unknown evaluation')
        if event['event']=='started' and eid not in starts:
            starts.add(eid)
        elif event['event']=='result' and eid in starts and eid not in results:
            results[eid]=event
        else:
            raise ValueError('invalid log sequence')
    if starts-set(results):
        raise ValueError('unfinished calls; wait before producing final tables')
    raw_attempts = list(results.values())
    recovery_hash = None
    if recovery is not None:
        from recover_requirement_auth_failures import load as load_recovery
        recovery_plan, _, recovery_mapping, _ = load_recovery(source, recovery)
        recovery_path = recovery/'judgments.v2.jsonl'
        recovered_events=list(map(json.loads,recovery_path.read_text(encoding='utf-8').splitlines()))
        if recovered_events[0] != recovery_plan:
            raise ValueError('recovery provenance mismatch')
        recovered_starts, recovered_results = set(), {}
        for event in recovered_events[1:]:
            eid=event['evaluation_id']
            if eid not in recovery_mapping:
                raise ValueError('unknown recovery evaluation')
            if event['event']=='started' and eid not in recovered_starts:
                recovered_starts.add(eid)
            elif event['event']=='result' and eid in recovered_starts and eid not in recovered_results:
                recovered_results[eid]=event
            else:
                raise ValueError('invalid recovery log sequence')
        if recovered_starts-set(recovered_results):
            raise ValueError('unfinished recovery call')
        for eid,event in recovered_results.items():
            original=results.get(eid)
            if not original or original['status']!='api_error' or original['http_status']!=401:
                raise ValueError('ineligible recovery')
            raw_attempts.append(event)
            # Replace only the analytical slot; original raw logs remain intact.
            results[eid]=event
        recovery_hash=sha256(recovery_path.read_bytes()).hexdigest()
        events=[plan]+[event for eid in sorted(results) for event in (
            {'event':'started','evaluation_id':eid},results[eid])]
    summary=summarize(events,mapping)
    by_job={r['job_id']:r for r in summary['responses']}
    header=json.loads((source/'generations.jsonl').read_text(encoding='utf-8').splitlines()[0])
    jobs={j['job_id']:j for j in header['jobs']}
    strata=sorted({(j.get('generator_id','unknown'),j['condition']) for j in jobs.values()})
    names=list(next(iter(jobs.values()))['payload'])
    requirement_rows=[];score_rows=[];operational=[];task_requirement_rows=[]
    for generator_id,condition in strata:
        ids={e for e,m in mapping.items() if m['condition']==condition and m.get('generator_id','unknown')==generator_id}
        selected=[results[e] for e in sorted(ids) if e in results]
        valid=[e for e in selected if e['status']=='success']
        jobids={mapping[e]['job_id'] for e in ids}
        complete=[by_job[j] for j in sorted(jobids) if j in by_job and by_job[j]['complete_triplet']]
        operational.append({'generator_id':generator_id,'condition':condition,'planned_judgments':len(ids),'completed':len(selected),
            'valid':len(valid),'statuses':dict(Counter(e['status'] for e in selected)),
            'planned_responses':len(jobids),'complete_triplets':len(complete),
            'unique_generated_texts':len({sha256(candidates[j].encode()).hexdigest() for j in jobids if j in candidates})})
        for name in names:
            counts=Counter(e['validated']['requirements'][name]['status'] for e in valid)
            row={'generator_id':generator_id,'condition':condition,'requirement':name,'valid_judgments':len(valid),
                **{state:counts[state] for state in ('supported','partial','not_addressed','contradicted','uncertain')},
                'complete_triplets':len(complete),
                'exact_agreement_triplets':sum(r['requirements'][name]['exact_agreement'] for r in complete)}
            requirement_rows.append(row)
        for task in sorted({jobs[j].get('task_id', j) for j in jobids}):
            task_valid=[e for e in valid if jobs[mapping[e['evaluation_id']]['job_id']].get('task_id',mapping[e['evaluation_id']]['job_id'])==task]
            for name in names:
                counts=Counter(e['validated']['requirements'][name]['status'] for e in task_valid)
                task_requirement_rows.append({'generator_id':generator_id,'task_id':task,'condition':condition,'requirement':name,
                    'valid_judgments':len(task_valid),**{state:counts[state] for state in ('supported','partial','not_addressed','contradicted','uncertain')}})
        for criterion in ('instructional_alignment','textual_coherence'):
            values=[r['assessments'][criterion]['median'] for r in complete]
            task_medians = {}
            for task in sorted({jobs[j].get('task_id', j) for j in jobids}):
                task_values=[by_job[j]['assessments'][criterion]['median'] for j in sorted(jobids)
                             if jobs[j].get('task_id', j)==task and j in by_job and by_job[j]['complete_triplet']]
                task_medians[task]=median(task_values) if task_values else None
            eligible_task_values=[v for v in task_medians.values() if v is not None]
            score_rows.append({'generator_id':generator_id,'condition':condition,'criterion':criterion,'complete_triplets':len(values),
                               'median_of_response_medians':median(values) if values else None,
                               'response_medians':values,'task_medians':task_medians,
                               'median_of_task_medians':median(eligible_task_values) if eligible_task_values else None,
                               'exact_agreement_triplets':sum(len(set(r['assessments'][criterion]['scores']))==1 for r in complete)})
    tables={'by_task_requirements':task_requirement_rows,'operational':operational,'requirements':requirement_rows,'secondary_scores':score_rows,
            'source_log_sha256':sha256((directory/'judgments.v2.jsonl').read_bytes()).hexdigest(),
            'planned_judgments':len(queue),'completed':len(results),
            'operational_attempts':len(raw_attempts),'attempt_statuses':dict(Counter(e['status'] for e in raw_attempts)),
            'recovery_log_sha256':recovery_hash,
            'usage':{name:{'reported_attempts':sum(isinstance((e.get('raw_response') or {}).get('usage',{}).get(name),int) for e in raw_attempts),
                           'sum':sum((e.get('raw_response') or {}).get('usage',{}).get(name) or 0 for e in raw_attempts)}
                     for name in ('input_tokens','output_tokens','total_tokens')},
            'source_generation_log_sha256':plan.get('source_log_sha256'),
            'configuration_hash':plan.get('configuration_hash'),
            'tasks':{j.get('task_id',j['job_id']):j['payload']['topic'] for j in jobs.values()},
            'study_phase':header.get('config',{}).get('study_phase','pilot'),
            'interpretation':'Descriptive by generator, task and condition. Dependent repetitions. No composite score, statistical significance, causal or pedagogical efficacy claim. Syntax and semantic estimates remain distinct.'}
    (directory/'results_tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (directory/'requirements_by_condition.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(requirement_rows[0]));writer.writeheader();writer.writerows(requirement_rows)
    with (directory/'requirements_by_task.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(task_requirement_rows[0]));writer.writeheader();writer.writerows(task_requirement_rows)
    lines=['# Resultados descritivos — contrato v2','',tables['interpretation'],'',
           f"Tentativas operacionais: {len(raw_attempts)}. Estados das tentativas: {tables['attempt_statuses']}. Avaliações únicas concluídas: {len(results)}/{len(queue)}.",'',
           '| Gerador | Condição | Julgamentos válidos/concluídos | Planos com três julgamentos válidos | Textos distintos |',
           '|---|---|---:|---:|---:|']
    for r in operational:
        lines.append(f"| {r['generator_id']} | {r['condition'].upper()} | {r['valid']}/{r['completed']} | {r['complete_triplets']}/{r['planned_responses']} | {r['unique_generated_texts']} |")
    lines+=['','Categorias nominais por requisito; denominador = julgamentos válidos. Não são scores de qualidade ou medidas de acurácia.','',
            '| Gerador | Condição | Requisito | Supported | Partial | Not addressed | Contradicted | Uncertain | Concordância exata/trincas |','|---|---|---|---:|---:|---:|---:|---:|---:|']
    for r in requirement_rows:
        lines.append('| '+ ' | '.join(str(r[k]) for k in ('generator_id','condition','requirement','supported','partial','not_addressed','contradicted','uncertain'))+f" | {r['exact_agreement_triplets']}/{r['complete_triplets']} |")
    lines+=['','Duas notas secundárias autorais, sem nota global:','', '| Gerador | Condição | Critério | Mediana das medianas por tarefa | Trincas completas | Concordância exata |','|---|---|---|---:|---:|---:|']
    for r in score_rows:
        lines.append(f"| {r['generator_id']} | {r['condition']} | {r['criterion']} | {r['median_of_task_medians']} | {r['complete_triplets']} | {r['exact_agreement_triplets']}/{r['complete_triplets']} |")
    lines+=['','C0 recebeu somente tópico e tipo de material. C1 e C2 receberam os mesmos sete requisitos. C0/C1 altera informação; C1/C2 altera organização. A falta de requisito em C0 não prova inferioridade do modelo.',
            '', 'Falhas e trincas incompletas não recebem zero. Resultados v1 e v2 não são comparados como a mesma escala. Não foi realizada avaliação com participantes humanos.']
    (directory/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return tables


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--recovery',type=Path)
    args=parser.parse_args()
    result=report(args.source,args.directory,args.recovery)
    print(json.dumps(result['operational']))
