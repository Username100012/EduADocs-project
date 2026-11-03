# Sete requisitos por modelo e condição — 27/10/2026

Análise descritiva dos julgamentos já salvos. Zero chamadas às APIs. Categorias nominais preservadas: supported, partial, not_addressed, contradicted e uncertain. Não há nota composta, conversão ordinal, voto por maioria ou teste de significância.

As proporções abaixo descrevem julgamentos válidos, não planos independentes nem acurácia. São frequências agrupadas com denominadores explícitos; não substituem a análise por tarefa e não são uma nova métrica principal com peso igual por tarefa. Falhas operacionais/de validação não entram no denominador e não recebem zero. As três avaliações de um mesmo texto são dependentes.

## Frequência da categoria supported

| Modelo | Requisito | C0 | C1 | C2 |
|---|---|---:|---:|---:|
| gemini | Tópico | 102/102 (100.0%) | 101/101 (100.0%) | 105/105 (100.0%) |
| gemini | Nível escolar | 48/102 (47.1%) | 101/101 (100.0%) | 105/105 (100.0%) |
| gemini | Objetivos | 26/102 (25.5%) | 101/101 (100.0%) | 105/105 (100.0%) |
| gemini | Duração | 12/102 (11.8%) | 101/101 (100.0%) | 105/105 (100.0%) |
| gemini | Metodologia | 63/102 (61.8%) | 101/101 (100.0%) | 105/105 (100.0%) |
| gemini | Materiais | 6/102 (5.9%) | 97/101 (96.0%) | 105/105 (100.0%) |
| gemini | Estratégia de avaliação | 0/102 (0.0%) | 101/101 (100.0%) | 105/105 (100.0%) |
| qwen3 | Tópico | 105/105 (100.0%) | 105/105 (100.0%) | 106/106 (100.0%) |
| qwen3 | Nível escolar | 27/105 (25.7%) | 105/105 (100.0%) | 106/106 (100.0%) |
| qwen3 | Objetivos | 0/105 (0.0%) | 99/105 (94.3%) | 96/106 (90.6%) |
| qwen3 | Duração | 0/105 (0.0%) | 77/105 (73.3%) | 68/106 (64.2%) |
| qwen3 | Metodologia | 43/105 (41.0%) | 105/105 (100.0%) | 106/106 (100.0%) |
| qwen3 | Materiais | 0/105 (0.0%) | 78/105 (74.3%) | 106/106 (100.0%) |
| qwen3 | Estratégia de avaliação | 0/105 (0.0%) | 95/105 (90.5%) | 101/106 (95.3%) |

## Interpretação do contraste C1/C2

- Gemini: seis requisitos têm 100% de supported em ambas as condições. Materiais passa de 97/101 para 105/105; em C1 há quatro partial. O resultado apresenta concentração no teto da classificação.
- Qwen3: tópico, nível escolar e metodologia têm 100% em ambas. Materiais passa de 78/105 para 106/106; estratégia de avaliação, de 95/105 para 101/106. Objetivos passa de 99/105 para 96/106; duração, de 77/105 para 68/106.
- As categorias restantes são necessárias à leitura: nos objetivos do Qwen3, C1 tem seis contradicted; C2 tem nove partial e um contradicted. Na duração, C1 tem 28 contradicted; C2 tem 21 contradicted e 17 uncertain. Menos supported não significa automaticamente mais contradições.
- Aumento de supported em materiais ocorre em cinco tarefas Qwen3 (006, 007, 009, 010 e 011). Em estratégia de avaliação há aumento nas tarefas 004 e 006, mas redução na 007. Não há melhoria uniforme.
- Nos objetivos do Qwen3, a tarefa 007 (GROUP BY/COUNT) passa de 9/9 supported em C1 para 0/9 em C2 (nove partial). A tarefa 012 (rastreabilidade) passa de 2/8 supported e seis contradicted para 8/9 supported e um contradicted. Os agregados ocultam essas direções diferentes.
- Na duração do Qwen3, supported diminui nas tarefas 002, 005, 006, 007 e 008; aumenta em 003, 004, 010, 011 e 012; permanece em 100% em 001 e 009. São comparações de frequências por tarefa, sem inferência de significância.
- Síntese: há um sinal descritivo favorável a C2 na explicitação dos materiais, mas os resultados dependem do requisito e da tarefa. Não há suporte para afirmar superioridade geral de C2. C0/C1 acrescenta informação; somente C1/C2 mantém os sete requisitos e altera a organização.

## Distribuições completas C1/C2

| Modelo | Condição | Requisito | Válidos | Supported | Partial | Not addressed | Contradicted | Uncertain | Concordância exata/trincas |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| gemini | C1 | Tópico | 101 | 101 | 0 | 0 | 0 | 0 | 32/32 |
| gemini | C1 | Nível escolar | 101 | 101 | 0 | 0 | 0 | 0 | 32/32 |
| gemini | C1 | Objetivos | 101 | 101 | 0 | 0 | 0 | 0 | 32/32 |
| gemini | C1 | Duração | 101 | 101 | 0 | 0 | 0 | 0 | 32/32 |
| gemini | C1 | Metodologia | 101 | 101 | 0 | 0 | 0 | 0 | 32/32 |
| gemini | C1 | Materiais | 101 | 97 | 4 | 0 | 0 | 0 | 31/32 |
| gemini | C1 | Estratégia de avaliação | 101 | 101 | 0 | 0 | 0 | 0 | 32/32 |
| gemini | C2 | Tópico | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| gemini | C2 | Nível escolar | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| gemini | C2 | Objetivos | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| gemini | C2 | Duração | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| gemini | C2 | Metodologia | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| gemini | C2 | Materiais | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| gemini | C2 | Estratégia de avaliação | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| qwen3 | C1 | Tópico | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| qwen3 | C1 | Nível escolar | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| qwen3 | C1 | Objetivos | 105 | 99 | 0 | 0 | 6 | 0 | 33/33 |
| qwen3 | C1 | Duração | 105 | 77 | 0 | 0 | 28 | 0 | 32/33 |
| qwen3 | C1 | Metodologia | 105 | 105 | 0 | 0 | 0 | 0 | 33/33 |
| qwen3 | C1 | Materiais | 105 | 78 | 22 | 0 | 0 | 5 | 30/33 |
| qwen3 | C1 | Estratégia de avaliação | 105 | 95 | 10 | 0 | 0 | 0 | 30/33 |
| qwen3 | C2 | Tópico | 106 | 106 | 0 | 0 | 0 | 0 | 34/34 |
| qwen3 | C2 | Nível escolar | 106 | 106 | 0 | 0 | 0 | 0 | 34/34 |
| qwen3 | C2 | Objetivos | 106 | 96 | 9 | 0 | 1 | 0 | 33/34 |
| qwen3 | C2 | Duração | 106 | 68 | 0 | 0 | 21 | 17 | 30/34 |
| qwen3 | C2 | Metodologia | 106 | 106 | 0 | 0 | 0 | 0 | 34/34 |
| qwen3 | C2 | Materiais | 106 | 106 | 0 | 0 | 0 | 0 | 34/34 |
| qwen3 | C2 | Estratégia de avaliação | 106 | 101 | 5 | 0 | 0 | 0 | 33/34 |

## Resultados por tarefa

Cada célula mostra supported/válidos. As demais categorias estão no CSV acompanhante e nas distribuições por tarefa de requirements_by_task.csv.

### gemini

| Tarefa | Requisito | C1 | C2 |
|---|---|---:|---:|
| task-001 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Materiais | 8/9 (88.9%) | 9/9 (100.0%) |
| task-001 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-002 | Tópico | 6/6 (100.0%) | 9/9 (100.0%) |
| task-002 | Nível escolar | 6/6 (100.0%) | 9/9 (100.0%) |
| task-002 | Objetivos | 6/6 (100.0%) | 9/9 (100.0%) |
| task-002 | Duração | 6/6 (100.0%) | 9/9 (100.0%) |
| task-002 | Metodologia | 6/6 (100.0%) | 9/9 (100.0%) |
| task-002 | Materiais | 3/6 (50.0%) | 9/9 (100.0%) |
| task-002 | Estratégia de avaliação | 6/6 (100.0%) | 9/9 (100.0%) |
| task-003 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-005 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-006 | Tópico | 7/7 (100.0%) | 8/8 (100.0%) |
| task-006 | Nível escolar | 7/7 (100.0%) | 8/8 (100.0%) |
| task-006 | Objetivos | 7/7 (100.0%) | 8/8 (100.0%) |
| task-006 | Duração | 7/7 (100.0%) | 8/8 (100.0%) |
| task-006 | Metodologia | 7/7 (100.0%) | 8/8 (100.0%) |
| task-006 | Materiais | 7/7 (100.0%) | 8/8 (100.0%) |
| task-006 | Estratégia de avaliação | 7/7 (100.0%) | 8/8 (100.0%) |
| task-007 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-010 | Tópico | 9/9 (100.0%) | 8/8 (100.0%) |
| task-010 | Nível escolar | 9/9 (100.0%) | 8/8 (100.0%) |
| task-010 | Objetivos | 9/9 (100.0%) | 8/8 (100.0%) |
| task-010 | Duração | 9/9 (100.0%) | 8/8 (100.0%) |
| task-010 | Metodologia | 9/9 (100.0%) | 8/8 (100.0%) |
| task-010 | Materiais | 9/9 (100.0%) | 8/8 (100.0%) |
| task-010 | Estratégia de avaliação | 9/9 (100.0%) | 8/8 (100.0%) |
| task-011 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-012 | Tópico | 7/7 (100.0%) | 8/8 (100.0%) |
| task-012 | Nível escolar | 7/7 (100.0%) | 8/8 (100.0%) |
| task-012 | Objetivos | 7/7 (100.0%) | 8/8 (100.0%) |
| task-012 | Duração | 7/7 (100.0%) | 8/8 (100.0%) |
| task-012 | Metodologia | 7/7 (100.0%) | 8/8 (100.0%) |
| task-012 | Materiais | 7/7 (100.0%) | 8/8 (100.0%) |
| task-012 | Estratégia de avaliação | 7/7 (100.0%) | 8/8 (100.0%) |

### qwen3

| Tarefa | Requisito | C1 | C2 |
|---|---|---:|---:|
| task-001 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-001 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-002 | Tópico | 9/9 (100.0%) | 8/8 (100.0%) |
| task-002 | Nível escolar | 9/9 (100.0%) | 8/8 (100.0%) |
| task-002 | Objetivos | 9/9 (100.0%) | 8/8 (100.0%) |
| task-002 | Duração | 9/9 (100.0%) | 0/8 (0.0%) |
| task-002 | Metodologia | 9/9 (100.0%) | 8/8 (100.0%) |
| task-002 | Materiais | 9/9 (100.0%) | 8/8 (100.0%) |
| task-002 | Estratégia de avaliação | 9/9 (100.0%) | 8/8 (100.0%) |
| task-003 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Duração | 3/9 (33.3%) | 9/9 (100.0%) |
| task-003 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-003 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-004 | Tópico | 8/8 (100.0%) | 9/9 (100.0%) |
| task-004 | Nível escolar | 8/8 (100.0%) | 9/9 (100.0%) |
| task-004 | Objetivos | 8/8 (100.0%) | 9/9 (100.0%) |
| task-004 | Duração | 6/8 (75.0%) | 9/9 (100.0%) |
| task-004 | Metodologia | 8/8 (100.0%) | 9/9 (100.0%) |
| task-004 | Materiais | 8/8 (100.0%) | 9/9 (100.0%) |
| task-004 | Estratégia de avaliação | 7/8 (87.5%) | 9/9 (100.0%) |
| task-005 | Tópico | 9/9 (100.0%) | 8/8 (100.0%) |
| task-005 | Nível escolar | 9/9 (100.0%) | 8/8 (100.0%) |
| task-005 | Objetivos | 9/9 (100.0%) | 8/8 (100.0%) |
| task-005 | Duração | 9/9 (100.0%) | 2/8 (25.0%) |
| task-005 | Metodologia | 9/9 (100.0%) | 8/8 (100.0%) |
| task-005 | Materiais | 9/9 (100.0%) | 8/8 (100.0%) |
| task-005 | Estratégia de avaliação | 9/9 (100.0%) | 8/8 (100.0%) |
| task-006 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-006 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-006 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-006 | Duração | 5/9 (55.6%) | 0/9 (0.0%) |
| task-006 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-006 | Materiais | 5/9 (55.6%) | 9/9 (100.0%) |
| task-006 | Estratégia de avaliação | 3/9 (33.3%) | 9/9 (100.0%) |
| task-007 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Objetivos | 9/9 (100.0%) | 0/9 (0.0%) |
| task-007 | Duração | 9/9 (100.0%) | 3/9 (33.3%) |
| task-007 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-007 | Materiais | 0/9 (0.0%) | 9/9 (100.0%) |
| task-007 | Estratégia de avaliação | 6/9 (66.7%) | 4/9 (44.4%) |
| task-008 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Duração | 3/9 (33.3%) | 0/9 (0.0%) |
| task-008 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Materiais | 9/9 (100.0%) | 9/9 (100.0%) |
| task-008 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Duração | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-009 | Materiais | 3/9 (33.3%) | 9/9 (100.0%) |
| task-009 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-010 | Tópico | 8/8 (100.0%) | 9/9 (100.0%) |
| task-010 | Nível escolar | 8/8 (100.0%) | 9/9 (100.0%) |
| task-010 | Objetivos | 8/8 (100.0%) | 9/9 (100.0%) |
| task-010 | Duração | 3/8 (37.5%) | 9/9 (100.0%) |
| task-010 | Metodologia | 8/8 (100.0%) | 9/9 (100.0%) |
| task-010 | Materiais | 3/8 (37.5%) | 9/9 (100.0%) |
| task-010 | Estratégia de avaliação | 8/8 (100.0%) | 9/9 (100.0%) |
| task-011 | Tópico | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Nível escolar | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Objetivos | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Duração | 6/9 (66.7%) | 9/9 (100.0%) |
| task-011 | Metodologia | 9/9 (100.0%) | 9/9 (100.0%) |
| task-011 | Materiais | 6/9 (66.7%) | 9/9 (100.0%) |
| task-011 | Estratégia de avaliação | 9/9 (100.0%) | 9/9 (100.0%) |
| task-012 | Tópico | 8/8 (100.0%) | 9/9 (100.0%) |
| task-012 | Nível escolar | 8/8 (100.0%) | 9/9 (100.0%) |
| task-012 | Objetivos | 2/8 (25.0%) | 8/9 (88.9%) |
| task-012 | Duração | 6/8 (75.0%) | 9/9 (100.0%) |
| task-012 | Metodologia | 8/8 (100.0%) | 9/9 (100.0%) |
| task-012 | Materiais | 8/8 (100.0%) | 9/9 (100.0%) |
| task-012 | Estratégia de avaliação | 8/8 (100.0%) | 9/9 (100.0%) |

## Limitações e rastreabilidade

As classificações são estimativas de uma única família de julgadora, repetida três vezes, sem padrão-ouro humano. A validação das citações comprova correspondência literal, não pertinência ou correção do julgamento. Supported em duração não certifica aritmeticamente o cronograma. Declarações sobre contradições e omissões acima são atribuídas à julgadora, sem auditoria factual independente adicional.

Não houve nova coleta, ajuste dos prompts, dos detectores ou do contrato. A condição Gemini C1 tem 35 planos por um timeout na geração; as demais têm 36. Os julgamentos válidos por condição são Gemini C0/C1/C2: 102/101/105; Qwen3: 105/105/106. Há 196 trincas completas entre 215 planos; a concordância usa somente essas trincas, sem descartar julgamentos válidos das frequências nominais.

### Catálogo das tarefas

- task-001: Maior elemento de um vetor não vazio.
- task-002: Contagem de números pares em um vetor.
- task-003: Uma passagem de trocas adjacentes em ordenação por bolha.
- task-004: Operações de pilha com política LIFO.
- task-005: Chaves primária e estrangeira em tabelas de pedidos.
- task-006: INNER JOIN entre clientes e pedidos.
- task-007: Agrupamento SQL com GROUP BY e COUNT.
- task-008: Primeira forma normal e atributos multivalorados.
- task-009: Caso de uso de reserva de uma quadra esportiva.
- task-010: Critérios de aceitação de aplicação de cupom em uma compra.
- task-011: Particionamento de equivalência para validação de idade.
- task-012: Rastreabilidade entre requisitos e testes de um aplicativo de entregas.

Auditoria computacional exploratória concluída: [casos, evidências e limitações](case-audit/AUDIT.md). Identificados defeitos dos planos, um erro aritmético verificável da julgadora e variação na interpretação de objetivos. Classificações principais preservadas; zero chamadas adicionais às APIs.
