"""Describe frozen nominal judgments by condition and task, without API calls."""
import csv
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'artifacts/main-judgments-v1'
STATES = ('supported', 'partial', 'not_addressed', 'contradicted', 'uncertain')
LABELS = dict(topic='Tópico', grade_level='Nível escolar',
              learning_objectives='Objetivos', duration_minutes='Duração',
              methodology='Metodologia', materials='Materiais',
              assessment_strategy='Estratégia de avaliação')


def main():
    source = DIRECTORY / 'results_tables.json'
    tables = json.loads(source.read_text(encoding='utf-8'))
    rows = tables['requirements']
    tasks = tables['by_task_requirements']
    assert tables['completed'] == 645 and tables['attempt_statuses']['success'] == 624
    assert sha256((DIRECTORY / 'judgments.v2.jsonl').read_bytes()).hexdigest() == tables['source_log_sha256']
    assert len(rows) == 42 and len(tasks) == 504
    for row in rows:
        selected = [r for r in tasks if all(r[k] == row[k] for k in
                    ('generator_id', 'condition', 'requirement'))]
        assert len(selected) == 12
        for key in (*STATES, 'valid_judgments'):
            assert sum(r[key] for r in selected) == row[key]
        assert sum(row[s] for s in STATES) == row['valid_judgments']
        for r in selected:
            assert sum(r[s] for s in STATES) == r['valid_judgments']

    def fraction(row):
        return f"{row['supported']}/{row['valid_judgments']} ({100 * row['supported'] / row['valid_judgments']:.1f}%)"

    lookup = {(r['generator_id'], r['condition'], r['requirement']): r for r in rows}
    task_lookup = {(r['generator_id'], r['task_id'], r['condition'], r['requirement']): r for r in tasks}
    comparisons = []
    for g in ('gemini', 'qwen3'):
        for task in sorted(tables['tasks']):
            for req in LABELS:
                a, b = [task_lookup[g, task, c, req] for c in ('c1', 'c2')]
                comparisons.append({'generator_id': g, 'task_id': task,
                    'topic': tables['tasks'][task], 'requirement': req,
                    **{f'{c}_{k}': r[k] for c, r in [('c1', a), ('c2', b)]
                       for k in ('valid_judgments', *STATES)}})
    with (DIRECTORY / 'c1_c2_requirements_by_task.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)

    lines = ['# Sete requisitos por modelo e condição — 27/10/2026', '',
        'Análise descritiva dos julgamentos já salvos. Zero chamadas às APIs. '
        'Categorias nominais preservadas: supported, partial, not_addressed, contradicted e uncertain. '
        'Não há nota composta, conversão ordinal, voto por maioria ou teste de significância.', '',
        'As proporções abaixo descrevem julgamentos válidos, não planos independentes nem acurácia. '
        'São frequências agrupadas com denominadores explícitos; não substituem a análise por tarefa '
        'e não são uma nova métrica principal com peso igual por tarefa. '
        'Falhas operacionais/de validação não entram no denominador e não recebem zero. '
        'As três avaliações de um mesmo texto são dependentes.', '',
        '## Frequência da categoria supported', '',
        '| Modelo | Requisito | C0 | C1 | C2 |', '|---|---|---:|---:|---:|']
    for g in ('gemini', 'qwen3'):
        for req, label in LABELS.items():
            lines.append(f'| {g} | {label} | ' + ' | '.join(fraction(lookup[g, c, req]) for c in ('c0', 'c1', 'c2')) + ' |')
    lines += ['', '## Interpretação do contraste C1/C2', '',
        '- Gemini: seis requisitos têm 100% de supported em ambas as condições. Materiais passa de 97/101 para 105/105; em C1 há quatro partial. O resultado apresenta concentração no teto da classificação.',
        '- Qwen3: tópico, nível escolar e metodologia têm 100% em ambas. Materiais passa de 78/105 para 106/106; estratégia de avaliação, de 95/105 para 101/106. Objetivos passa de 99/105 para 96/106; duração, de 77/105 para 68/106.',
        '- As categorias restantes são necessárias à leitura: nos objetivos do Qwen3, C1 tem seis contradicted; C2 tem nove partial e um contradicted. Na duração, C1 tem 28 contradicted; C2 tem 21 contradicted e 17 uncertain. Menos supported não significa automaticamente mais contradições.',
        '- Aumento de supported em materiais ocorre em cinco tarefas Qwen3 (006, 007, 009, 010 e 011). Em estratégia de avaliação há aumento nas tarefas 004 e 006, mas redução na 007. Não há melhoria uniforme.',
        '- Nos objetivos do Qwen3, a tarefa 007 (GROUP BY/COUNT) passa de 9/9 supported em C1 para 0/9 em C2 (nove partial). A tarefa 012 (rastreabilidade) passa de 2/8 supported e seis contradicted para 8/9 supported e um contradicted. Os agregados ocultam essas direções diferentes.',
        '- Na duração do Qwen3, supported diminui nas tarefas 002, 005, 006, 007 e 008; aumenta em 003, 004, 010, 011 e 012; permanece em 100% em 001 e 009. São comparações de frequências por tarefa, sem inferência de significância.',
        '- Síntese: há um sinal descritivo favorável a C2 na explicitação dos materiais, mas os resultados dependem do requisito e da tarefa. Não há suporte para afirmar superioridade geral de C2. C0/C1 acrescenta informação; somente C1/C2 mantém os sete requisitos e altera a organização.', '',
        '## Distribuições completas C1/C2', '',
        '| Modelo | Condição | Requisito | Válidos | Supported | Partial | Not addressed | Contradicted | Uncertain | Concordância exata/trincas |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        if r['condition'] in ('c1', 'c2'):
            lines.append('| ' + ' | '.join(str(v) for v in [r['generator_id'], r['condition'].upper(), LABELS[r['requirement']], r['valid_judgments'], *(r[s] for s in STATES), f"{r['exact_agreement_triplets']}/{r['complete_triplets']}"]) + ' |')
    lines += ['', '## Resultados por tarefa', '',
        'Cada célula mostra supported/válidos. As demais categorias estão no CSV acompanhante e nas distribuições por tarefa de requirements_by_task.csv.']
    for g in ('gemini', 'qwen3'):
        lines += ['', f'### {g}', '', '| Tarefa | Requisito | C1 | C2 |', '|---|---|---:|---:|']
        for task in sorted(tables['tasks']):
            for req, label in LABELS.items():
                lines.append(f'| {task} | {label} | {fraction(task_lookup[g, task, "c1", req])} | {fraction(task_lookup[g, task, "c2", req])} |')
    lines += ['', '## Limitações e rastreabilidade', '',
        'As classificações são estimativas de uma única família de julgadora, repetida três vezes, sem padrão-ouro humano. '
        'A validação das citações comprova correspondência literal, não pertinência ou correção do julgamento. '
        'Supported em duração não certifica aritmeticamente o cronograma. '
        'Declarações sobre contradições e omissões acima são atribuídas à julgadora, sem auditoria factual independente adicional.', '',
        'Não houve nova coleta, ajuste dos prompts, dos detectores ou do contrato. '
        'A condição Gemini C1 tem 35 planos por um timeout na geração; as demais têm 36. '
        'Os julgamentos válidos por condição são Gemini C0/C1/C2: 102/101/105; Qwen3: 105/105/106. '
        'Há 196 trincas completas entre 215 planos; a concordância usa somente essas trincas, sem descartar julgamentos válidos das frequências nominais.', '',
        '### Catálogo das tarefas', '']
    lines += [f'- {task}: {topic}.' for task, topic in sorted(tables['tasks'].items())]
    (DIRECTORY / 'REQUIREMENTS_COMPARISON.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    audit = {'api_calls': 0, 'source_tables_sha256': sha256(source.read_bytes()).hexdigest(),
             'source_judgment_log_sha256': tables['source_log_sha256'],
             'condition_requirement_rows_verified': len(rows), 'task_requirement_rows_verified': len(tasks),
             'paired_task_requirement_rows': len(comparisons),
             'nominal_counts_preserved': True, 'task_totals_match_condition_totals': True,
             'no_hypothesis_tests_or_composite_scores': True}
    (DIRECTORY / 'requirements_comparison_audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(audit))


if __name__ == '__main__':
    main()
