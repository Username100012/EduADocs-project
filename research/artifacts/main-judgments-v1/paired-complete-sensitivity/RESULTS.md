# Sensibilidade C1/C2 — pares com trincas completas

Análise complementar pós-coleta, sem APIs e sem alteração dos resultados principais. Pareamento por gerador, tarefa e número de repetição de geração; só entram pares cujos dois planos têm três julgamentos válidos. Nenhuma decisão nominal por maioria e nenhum score composto.

## Cobertura

| Gerador | Pares incluídos/previstos | Julgamentos por condição | Tarefas representadas |
|---|---:|---:|---:|
| gemini | 30/36 | 90 | 12/12 |
| qwen3 | 31/36 | 93 | 12/12 |

## Notas ordinais

Mediana dos três julgamentos por plano, mediana por tarefa e mediana entre tarefas, como na análise principal. Só a seleção dos planos muda.

| Gerador | Condição | Critério | Principal | Pares completos |
|---|---|---|---:|---:|
| gemini | c1 | instructional_alignment | 4 | 4 |
| gemini | c1 | textual_coherence | 4 | 4 |
| gemini | c2 | instructional_alignment | 4 | 4 |
| gemini | c2 | textual_coherence | 4 | 4 |
| qwen3 | c1 | instructional_alignment | 4 | 4 |
| qwen3 | c1 | textual_coherence | 3 | 3 |
| qwen3 | c2 | instructional_alignment | 4 | 4 |
| qwen3 | c2 | textual_coherence | 3 | 3 |

## Supported por requisito

Proporções de julgamentos válidos dependentes, não acurácia nem proporção de planos independentes. A frequência das outras quatro categorias é preservada nos CSVs. Cada tarefa pode contribuir com 1–3 pares; frequências agrupadas não recebem automaticamente peso igual por tarefa.

| Gerador | Requisito | Principal C1 | Principal C2 | Pares C1 | Pares C2 |
|---|---|---:|---:|---:|---:|
| gemini | topic | 101/101 (100.0%) | 105/105 (100.0%) | 90/90 (100.0%) | 90/90 (100.0%) |
| gemini | grade_level | 101/101 (100.0%) | 105/105 (100.0%) | 90/90 (100.0%) | 90/90 (100.0%) |
| gemini | learning_objectives | 101/101 (100.0%) | 105/105 (100.0%) | 90/90 (100.0%) | 90/90 (100.0%) |
| gemini | duration_minutes | 101/101 (100.0%) | 105/105 (100.0%) | 90/90 (100.0%) | 90/90 (100.0%) |
| gemini | methodology | 101/101 (100.0%) | 105/105 (100.0%) | 90/90 (100.0%) | 90/90 (100.0%) |
| gemini | materials | 97/101 (96.0%) | 105/105 (100.0%) | 86/90 (95.6%) | 90/90 (100.0%) |
| gemini | assessment_strategy | 101/101 (100.0%) | 105/105 (100.0%) | 90/90 (100.0%) | 90/90 (100.0%) |
| qwen3 | topic | 105/105 (100.0%) | 106/106 (100.0%) | 93/93 (100.0%) | 93/93 (100.0%) |
| qwen3 | grade_level | 105/105 (100.0%) | 106/106 (100.0%) | 93/93 (100.0%) | 93/93 (100.0%) |
| qwen3 | learning_objectives | 99/105 (94.3%) | 96/106 (90.6%) | 87/93 (93.5%) | 83/93 (89.2%) |
| qwen3 | duration_minutes | 77/105 (73.3%) | 68/106 (64.2%) | 71/93 (76.3%) | 57/93 (61.3%) |
| qwen3 | methodology | 105/105 (100.0%) | 106/106 (100.0%) | 93/93 (100.0%) | 93/93 (100.0%) |
| qwen3 | materials | 78/105 (74.3%) | 106/106 (100.0%) | 67/93 (72.0%) | 93/93 (100.0%) |
| qwen3 | assessment_strategy | 95/105 (90.5%) | 101/106 (95.3%) | 83/93 (89.2%) | 88/93 (94.6%) |

## Pares excluídos

A exclusão afeta o par inteiro, inclusive o plano sem falha na condição oposta. Não houve reenvio nem atribuição de zero.

- gemini/task-002/r1: {'c1': 'generation_error'}.
- gemini/task-006/r1: {'c1': 'incomplete_judgment_triplet'}.
- gemini/task-006/r3: {'c1': 'incomplete_judgment_triplet', 'c2': 'incomplete_judgment_triplet'}.
- gemini/task-010/r1: {'c2': 'incomplete_judgment_triplet'}.
- gemini/task-012/r1: {'c1': 'incomplete_judgment_triplet'}.
- gemini/task-012/r2: {'c2': 'incomplete_judgment_triplet'}.
- qwen3/task-002/r2: {'c2': 'incomplete_judgment_triplet'}.
- qwen3/task-004/r2: {'c1': 'incomplete_judgment_triplet'}.
- qwen3/task-005/r2: {'c2': 'incomplete_judgment_triplet'}.
- qwen3/task-010/r3: {'c1': 'incomplete_judgment_triplet'}.
- qwen3/task-012/r2: {'c1': 'incomplete_judgment_triplet'}.

## Limites

Esta análise equilibra os denominadores C1/C2 e preserva as mesmas tarefas/repetições em ambas, mas não prova ausência de viés dos dados ausentes. Casos completos podem ser selecionados de forma não aleatória. As repetições permanecem dependentes; o rótulo r1/r2/r3 não é garantia de sorteio comum entre condições. Não houve teste de significância, equivalência ou recalibração dos instrumentos. O protocolo principal e todos os erros permanecem preservados.

## Interpretação da sensibilidade

O recorte preservou as 12 tarefas em ambos os geradores. As medianas gerais dos critérios secundários permaneceram iguais às da análise principal: alinhamento 4 em C1 e C2 nos dois modelos, coerência 4 no Gemini e 3 no Qwen3.

No Gemini, os seis requisitos anteriormente no teto continuam com 100% de supported; materiais fica em 86/90 (95,6%) em C1 e 90/90 (100%) em C2. No Qwen3, materiais fica em 67/93 (72,0%) versus 93/93 (100%); estratégia de avaliação, 83/93 (89,2%) versus 88/93 (94,6%); objetivos, 87/93 (93,5%) versus 83/93 (89,2%); duração, 71/93 (76,3%) versus 57/93 (61,3%). Tópico, nível escolar e metodologia mantêm 100% nas duas condições.

Portanto, equilibrar os pares não inverte as direções dos contrastes agrupados observados nos sete requisitos. A interpretação de efeitos mistos e ausência de superioridade geral demonstrada de C2 é mantida neste recorte. Isso não prova equivalência, ausência de viés de seleção ou estabilidade em outros padrões de dados ausentes. Não é uma análise de pior caso nem uma correção dos erros da julgadora.
