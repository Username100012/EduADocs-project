"""Consolidate frozen structural/operational measures; never call an API.

This implements the pre-collection descriptive aggregation, not a new detector.
"""
import argparse
from collections import Counter
import csv
from hashlib import sha256
from decimal import Decimal
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from experiment.main_protocol import verify_frozen
from experiment.requirement_measurement import LABELS,VERSION
from observe_saved_requirements import observe
from evaluate_pilot import evaluate
from summarize_primary_metrics import distribution


def reported_google_cost(response, pricing):
    """Gross estimate from reported total usage; no cache discount or billing claim."""
    if not response or response.get('provider') != 'google':
        return None
    incoming=response.get('input_tokens');visible=response.get('output_tokens')
    total=(response.get('raw_metadata') or {}).get('total_tokens')
    if any(type(v) is not int or v<0 for v in (incoming,visible,total)) or total<incoming+visible:
        return None
    generated=total-incoming  # Thinking + visible output; tools/history are disabled by protocol.
    usd=(Decimal(incoming)*Decimal(str(pricing['input_usd_per_million_tokens']))+
         Decimal(generated)*Decimal(str(pricing['output_usd_per_million_tokens_including_thinking'])))/Decimal(1_000_000)
    return str(usd)


def aggregate(selected, planned):
    available=[r for r in selected if r['observation'] is not None]
    n=len(available)
    fields={}
    for name in LABELS:
        counts=Counter(r['observation']['fields'][name]['observation'] for r in available)
        fields[name]={'denominator':n,'counts':{state:counts[state] for state in ('detected','empty','not_detected')},
                      'proportions':{state:counts[state]/n if n else None for state in ('detected','empty','not_detected')}}
    durations=[r['observation']['duration'] for r in available]
    duration={name:{'true':sum(r[name] is True for r in durations),
                    'false':sum(r[name] is False for r in durations),
                    'unknown':sum(r[name] is None for r in durations),'denominator':n}
              for name in ('declared_matches_target','schedule_matches_target','target_mismatch_detected','internal_inconsistency_detected')}
    duration['declared_value_available']=sum(bool(r['declared']) for r in durations)
    duration['clock_schedule_available']=sum(r['clock_schedule_minutes'] is not None for r in durations)
    operational={name:distribution([r['operational'].get(name) for r in selected if r['operational'] is not None])
                 for name in ('latency_ms','input_tokens','output_tokens')}
    operational['word_count']=distribution([r['word_count'] for r in available])
    return {'planned':planned,'completed':len(selected),'analyzable_texts':n,'results_without_text':len(selected)-n,
            'statuses':dict(sorted(Counter(r['status'] for r in selected).items())),
            'unique_texts':len({r['content_sha256'] for r in available}),
            'fields':fields,'duration':duration,'operational':operational,
            'reported_google_cost_estimate':{'available':sum(r.get('google_cost_usd') is not None for r in selected),
                'usd_sum':str(sum((Decimal(r['google_cost_usd']) for r in selected if r.get('google_cost_usd') is not None),Decimal(0))) if any(r.get('google_cost_usd') is not None for r in selected) else None}}


def summarize(directory):
    config=verify_frozen(ROOT/'experiments/main_config.json')
    log=directory/'generations.jsonl';source_hash=sha256(log.read_bytes()).hexdigest()
    collection=json.loads((directory/'collection_summary.json').read_text(encoding='utf-8'))
    if collection['source_log_sha256']!=source_hash or collection['completed']!=216:
        raise ValueError('collection changed or is incomplete')
    events=list(map(json.loads,log.read_text(encoding='utf-8').splitlines()))
    if events[0]['config']!=config or events[0]['simulated']:
        raise ValueError('wrong main configuration or simulated source')
    metrics=evaluate(log,version='v2')  # Existing frozen lexical instrument: word count + operations only here.
    observations=observe(directory)
    if observations['source_log_sha256']!=source_hash:
        raise ValueError('observations source mismatch')
    auxiliary={r['job_id']:r for r in metrics['records']}
    jobs=events[0]['jobs'];rows=[]
    raw_results={e['job_id']:e for e in events[1:] if e['event']=='result'}
    for row in observations['records']:
        m=auxiliary[row['job_id']]
        rows.append({**row,'operational':m['operational'],'word_count':m['metrics']['word_count'] if m['metrics'] else None,
                     'content_sha256':m['content_sha256'],
                     'google_cost_usd':reported_google_cost(raw_results[row['job_id']]['response'],config['generators']['gemini']['pricing_reference'])})
    groups=[]
    for task in [None]+sorted({j['task_id'] for j in jobs}):
        for generator,condition in sorted({(j['generator_id'],j['condition']) for j in jobs}):
            selected=[r for r in rows if r['generator_id']==generator and r['condition']==condition and (task is None or r['task_id']==task)]
            planned=sum(j['generator_id']==generator and j['condition']==condition and (task is None or j['task_id']==task) for j in jobs)
            group={'task_id':task,'subject':next((j['subject'] for j in jobs if j['task_id']==task),None),
                   'generator_id':generator,'condition':condition,**aggregate(selected,planned)}
            if task is None:
                group['task_balanced_operations']={}
                for name in ('latency_ms','input_tokens','output_tokens','word_count'):
                    medians=[]
                    for tid in sorted({r['task_id'] for r in selected}):
                        task_rows=[r for r in selected if r['task_id']==tid]
                        values=([r['word_count'] for r in task_rows if r['observation'] is not None] if name=='word_count' else
                                [r['operational'].get(name) for r in task_rows if r['operational'] is not None])
                        medians.append(distribution(values)['median'])
                    group['task_balanced_operations'][name]=distribution(medians)
            groups.append(group)
    report={'report_version':'eduadocs-main-observations-summary-v1','measurement_version':VERSION,
            'source_log_sha256':source_hash,'source_observations_sha256':sha256((directory/'requirement_observations.v1.json').read_bytes()).hexdigest(),
            'summary_code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'distribution_code_sha256':sha256((ROOT/'scripts/summarize_primary_metrics.py').read_bytes()).hexdigest(),
            'groups':groups,'api_calls':0,'judgments_executed':0,'simulated':False,
            'interpretation':'Frozen syntactic detector and numeric extraction. No semantic adherence, pedagogical quality or global score. All tasks shown; repetitions are dependent.',
            'aggregation_note':'Implementation of the frozen descriptive plan after collection; no detector, alias, target, threshold or frozen source modified.',
            'quartiles':'statistics.quantiles inclusive; missing values excluded with available denominators reported',
            'cost_pricing_reference':config['generators']['gemini']['pricing_reference'],
            'cost_note':'Google gross estimate from reported input and (total minus input) tokens, including thinking, at frozen reference rates. No cache discount assumed, no actual invoice. Timeout cost unknown; local electricity not measured; OpenAI not called.'}
    (directory/'automatic_summary.v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=[];ops=[];times=[]
    for g in groups:
        key={k:g[k] for k in ('task_id','subject','generator_id','condition')}
        for name,v in g['fields'].items():
            fields.append({**key,'requirement':name,'analyzable_texts':v['denominator'],
                           'results_without_text':g['results_without_text'],**v['counts']})
        for name,v in g['operational'].items():ops.append({**key,'measure':name,'aggregation':'response_distribution',**v})
        for name,v in g.get('task_balanced_operations',{}).items():
            ops.append({**key,'measure':name,'aggregation':'equal_task_medians',**v})
        for name,v in g['duration'].items():
            if isinstance(v,dict):times.append({**key,'measure':name,**v})
    for name,table in [('automatic_fields.v1.csv',fields),('automatic_operations.v1.csv',ops),('automatic_duration.v1.csv',times)]:
        with (directory/name).open('w',encoding='utf-8-sig',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(table[0]));writer.writeheader();writer.writerows(table)
    overall=[g for g in groups if g['task_id'] is None]
    fmt=lambda x:'—' if x is None else f'{x:.2f}'
    lines=['# Indicadores automáticos — coleta principal','',
        'Análise local das 216 tentativas e 215 textos, sem chamadas às APIs. O timeout permanece separado. Campos detectados não equivalem a requisitos atendidos; campos não detectados não comprovam omissão.','',
        '| Gerador | Condição | Textos/tentativas | Textos distintos | Mediana entre tarefas: latência (s) | IQR entre tarefas (s) | Entrada mediana entre tarefas | Saída mediana entre tarefas |',
        '|---|---|---:|---:|---:|---:|---:|---:|']
    for g in overall:
        lat=g['task_balanced_operations']['latency_ms']
        lines.append(f"| {g['generator_id']} | {g['condition'].upper()} | {g['analyzable_texts']}/{g['completed']} | {g['unique_texts']} | {fmt(lat['median']/1000 if lat['median'] is not None else None)} | {fmt(lat['iqr']/1000 if lat['iqr'] is not None else None)} | {fmt(g['task_balanced_operations']['input_tokens']['median'])} | {fmt(g['task_balanced_operations']['output_tokens']['median'])} |")
    lines+=['','A tabela usa medianas por tarefa e depois mediana entre tarefas, com pesos iguais. JSON/CSV também preservam a distribuição entre respostas. Latência e tokens têm denominadores de disponibilidade no JSON/CSV. O timeout não recebe duração ou tokens zero. Tokens usam os tokenizadores de cada fornecedor; saída reportada não é uma contagem de palavras nem uma fatura.','',
        '| Gerador | Condição | Requisito | Detectado | Vazio | Não detectado | Textos analisáveis |','|---|---|---|---:|---:|---:|---:|']
    for g in overall:
        for name,v in g['fields'].items():
            c=v['counts'];lines.append(f"| {g['generator_id']} | {g['condition'].upper()} | {name} | {c['detected']} | {c['empty']} | {c['not_detected']} | {v['denominator']} |")
    lines+=['','## Duração numérica extraível','',
        '| Gerador | Condição | Declaração igual ao alvo | Diferente | Indeterminada | Divergência numérica detectada |','|---|---|---:|---:|---:|---:|']
    for g in overall:
        d=g['duration']['declared_matches_target'];m=g['duration']['target_mismatch_detected']
        lines.append(f"| {g['generator_id']} | {g['condition'].upper()} | {d['true']} | {d['false']} | {d['unknown']} | {m['true']} |")
    lines+=['','O extrator congelado reconhece declarações e intervalos HH:MM contíguos; não soma títulos arbitrários de etapas. Declaração de 50 minutos não demonstra cronograma consistente. Sem divergência detectada não se conclui consistência.','',
        'Os CSVs também separam cada uma das 12 tarefas. Não há teste de significância, score composto, avaliação factual ou conclusão de superioridade semântica de C2. C0 não recebeu seis requisitos-alvo; C1/C2 partilham o mesmo payload. Repetições e textos duplicados não são tarefas independentes.','',
        'O estado empty significa que as regras não associaram conteúdo ao rótulo reconhecido; não prova que a seção esteja realmente vazia. A detecção de campos requer padrões de rótulo previstos. Baixa detecção pode refletir formatação ou paráfrase. Esta etapa não recalibra o observador com as respostas principais. A estimativa semântica cabe à etapa posterior de julgamentos.']
    lines+=['','## Estimativa de custo Gemini','',
            'Estimativa bruta para as respostas com consumo reportado, usando a tabela congelada: US$ 0,75/milhão de entrada e US$ 3,75/milhão de saída, incluindo raciocínio. A saída faturável é inferida como total_tokens menos input_tokens. Não é fatura; não se presume desconto de cache. O custo do timeout é desconhecido e não recebe zero. Energia local não foi medida.','',
            '| Condição | Respostas com consumo disponível | Estimativa bruta USD |','|---|---:|---:|']
    for g in overall:
        if g['generator_id']=='gemini':
            c=g['reported_google_cost_estimate']
            lines.append(f"| {g['condition'].upper()} | {c['available']}/{g['completed']} | {c['usd_sum']} |")
    (directory/'AUTOMATIC_METRICS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);args=parser.parse_args()
    result=summarize(args.directory)
    print(json.dumps({'groups':len(result['groups']),'api_calls':result['api_calls'],
                     'overall':[{k:g[k] for k in ('generator_id','condition','analyzable_texts','results_without_text')} for g in result['groups'] if g['task_id'] is None]}))
