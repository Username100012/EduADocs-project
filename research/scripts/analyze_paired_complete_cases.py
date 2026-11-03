"""Post-hoc C1/C2 sensitivity analysis on matched complete judgment triplets. No APIs."""
import csv
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'artifacts/main-judgments-v1'
STATES = ('supported', 'partial', 'not_addressed', 'contradicted', 'uncertain')


def main():
    files = [ROOT/'artifacts/main-study-v1/generations.jsonl', DIRECTORY/'judgments.v2.jsonl',
             DIRECTORY/'summary.v2.json', DIRECTORY/'results_tables.json']
    hashes = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}
    generations = [json.loads(l) for l in files[0].read_text(encoding='utf-8').splitlines()]
    jobs = {j['job_id']: j for j in generations[0]['jobs']}
    gen_results = {r['job_id']:r for r in generations if r.get('event')=='result'}
    summaries = {r['job_id']:r for r in json.loads(files[2].read_text(encoding='utf-8'))['responses']}
    tables = json.loads(files[3].read_text(encoding='utf-8'))
    assert hashes[str(files[0].relative_to(ROOT))] == tables['source_generation_log_sha256']
    assert hashes[str(files[1].relative_to(ROOT))] == tables['source_log_sha256']
    pairs = []
    for generator in ('gemini', 'qwen3'):
        for task in sorted(tables['tasks']):
            for repetition in (1, 2, 3):
                ids = {c:f'{generator}:{task}:{c}:r{repetition}' for c in ('c1', 'c2')}
                reasons = {}
                for c, jid in ids.items():
                    assert jid in jobs
                    generation = gen_results[jid]
                    if generation['status'] != 'success':
                        reasons[c] = 'generation_' + generation['status']
                    elif not summaries.get(jid, {}).get('complete_triplet'):
                        reasons[c] = 'incomplete_judgment_triplet'
                pairs.append({'generator_id':generator, 'task_id':task, 'generation_repetition':repetition,
                              'job_ids':ids, 'included':not reasons, 'exclusion_reasons':reasons})
    requirements = []
    scores = []
    by_task = []
    coverage = []
    names = [r['requirement'] for r in tables['requirements'] if r['generator_id']=='gemini' and r['condition']=='c1']
    for generator in ('gemini', 'qwen3'):
        selected = [p for p in pairs if p['generator_id']==generator and p['included']]
        tasks = sorted({p['task_id'] for p in selected})
        coverage.append({'generator_id':generator, 'planned_pairs':36, 'included_pairs':len(selected),
                         'excluded_pairs':36-len(selected), 'represented_tasks':len(tasks),
                         'pairs_per_task':dict(Counter(p['task_id'] for p in selected))})
        for condition in ('c1', 'c2'):
            responses = [summaries[p['job_ids'][condition]] for p in selected]
            assert all(r['complete_triplet'] and r['valid']==3 for r in responses)
            for name in names:
                counts = Counter()
                for response in responses:
                    counts.update(response['requirements'][name]['frequencies'])
                assert sum(counts.values()) == 3*len(selected)
                requirements.append({'generator_id':generator,'condition':condition,'requirement':name,
                    'valid_judgments':3*len(selected), **{s:counts[s] for s in STATES}})
                for task in tasks:
                    task_responses = [summaries[p['job_ids'][condition]] for p in selected if p['task_id']==task]
                    task_counts=Counter()
                    for response in task_responses:
                        task_counts.update(response['requirements'][name]['frequencies'])
                    by_task.append({'generator_id':generator,'task_id':task,'condition':condition,
                        'requirement':name,'valid_judgments':3*len(task_responses),**{s:task_counts[s] for s in STATES}})
            for criterion in ('instructional_alignment','textual_coherence'):
                task_medians = {task:median(summaries[p['job_ids'][condition]]['assessments'][criterion]['median']
                    for p in selected if p['task_id']==task) for task in tasks}
                original = next(r for r in tables['secondary_scores'] if
                    (r['generator_id'],r['condition'],r['criterion'])==(generator,condition,criterion))
                scores.append({'generator_id':generator,'condition':condition,'criterion':criterion,
                    'paired_complete_median_of_task_medians':median(task_medians.values()),
                    'primary_median_of_task_medians':original['median_of_task_medians'],
                    'task_medians':task_medians})
    out = DIRECTORY/'paired-complete-sensitivity'
    out.mkdir(exist_ok=True)
    result={'analysis':'post-hoc matched complete-case sensitivity; not the frozen primary analysis',
            'api_calls':0,'matching_rule':'generator + task + generation repetition; both conditions require 3 valid judgments',
            'caveat':'Replicate labels are administrative matches, not proof of independent or coupled stochastic draws. Complete-case selection may be informative.',
            'coverage':coverage,'pairs':pairs,'requirements':requirements,'by_task_requirements':by_task,
            'secondary_scores':scores,'source_sha256':hashes}
    (out/'analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,rows in [('requirements.csv',requirements),('requirements_by_task.csv',by_task)]:
        with (out/name).open('w',encoding='utf-8-sig',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    lines=['# Sensibilidade C1/C2 — pares com trincas completas','','Análise complementar pós-coleta, sem APIs e sem alteração dos resultados principais. Pareamento por gerador, tarefa e número de repetição de geração; só entram pares cujos dois planos têm três julgamentos válidos. Nenhuma decisão nominal por maioria e nenhum score composto.','','## Cobertura','','| Gerador | Pares incluídos/previstos | Julgamentos por condição | Tarefas representadas |','|---|---:|---:|---:|']
    for r in coverage:lines.append(f"| {r['generator_id']} | {r['included_pairs']}/36 | {3*r['included_pairs']} | {r['represented_tasks']}/12 |")
    lines+=['','## Notas ordinais','','Mediana dos três julgamentos por plano, mediana por tarefa e mediana entre tarefas, como na análise principal. Só a seleção dos planos muda.','','| Gerador | Condição | Critério | Principal | Pares completos |','|---|---|---|---:|---:|']
    for r in scores:lines.append(f"| {r['generator_id']} | {r['condition']} | {r['criterion']} | {r['primary_median_of_task_medians']:g} | {r['paired_complete_median_of_task_medians']:g} |")
    lines+=['','## Supported por requisito','','Proporções de julgamentos válidos dependentes, não acurácia nem proporção de planos independentes. A frequência das outras quatro categorias é preservada nos CSVs. Cada tarefa pode contribuir com 1–3 pares; frequências agrupadas não recebem automaticamente peso igual por tarefa.','','| Gerador | Requisito | Principal C1 | Principal C2 | Pares C1 | Pares C2 |','|---|---|---:|---:|---:|---:|']
    def cell(r):return f"{r['supported']}/{r['valid_judgments']} ({100*r['supported']/r['valid_judgments']:.1f}%)"
    for generator in ('gemini','qwen3'):
        for name in names:
            key=lambda r:r['generator_id']==generator and r['requirement']==name
            primary=[next(r for r in tables['requirements'] if key(r) and r['condition']==c) for c in ('c1','c2')]
            paired=[next(r for r in requirements if key(r) and r['condition']==c) for c in ('c1','c2')]
            lines.append(f"| {generator} | {name} | "+' | '.join(cell(r) for r in primary+paired)+' |')
    lines+=['','## Pares excluídos','','A exclusão afeta o par inteiro, inclusive o plano sem falha na condição oposta. Não houve reenvio nem atribuição de zero.','']
    lines += [f"- {p['generator_id']}/{p['task_id']}/r{p['generation_repetition']}: {p['exclusion_reasons']}." for p in pairs if not p['included']]
    lines+=['','## Limites','','Esta análise equilibra os denominadores C1/C2 e preserva as mesmas tarefas/repetições em ambas, mas não prova ausência de viés dos dados ausentes. Casos completos podem ser selecionados de forma não aleatória. As repetições permanecem dependentes; o rótulo r1/r2/r3 não é garantia de sorteio comum entre condições. Não houve teste de significância, equivalência ou recalibração dos instrumentos. O protocolo principal e todos os erros permanecem preservados.']
    (out/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    assert all(sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in hashes.items())
    print(json.dumps({'coverage':coverage,'scores':scores,'requirements':requirements},ensure_ascii=False))


if __name__=='__main__':
    main()
