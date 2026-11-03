# Indicadores automáticos — coleta principal

Análise local das 216 tentativas e 215 textos, sem chamadas às APIs. O timeout permanece separado. Campos detectados não equivalem a requisitos atendidos; campos não detectados não comprovam omissão.

| Gerador | Condição | Textos/tentativas | Textos distintos | Mediana entre tarefas: latência (s) | IQR entre tarefas (s) | Entrada mediana entre tarefas | Saída mediana entre tarefas |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini | C0 | 36/36 | 36 | 18.08 | 2.13 | 23.00 | 1568.50 |
| gemini | C1 | 35/36 | 35 | 15.96 | 2.62 | 135.50 | 1335.50 |
| gemini | C2 | 36/36 | 36 | 14.89 | 1.98 | 189.50 | 1149.00 |
| qwen3 | C0 | 36/36 | 29 | 23.02 | 3.75 | 40.00 | 1146.00 |
| qwen3 | C1 | 36/36 | 29 | 28.19 | 3.05 | 177.00 | 1360.00 |
| qwen3 | C2 | 36/36 | 24 | 23.38 | 3.44 | 235.00 | 1133.50 |

A tabela usa medianas por tarefa e depois mediana entre tarefas, com pesos iguais. JSON/CSV também preservam a distribuição entre respostas. Latência e tokens têm denominadores de disponibilidade no JSON/CSV. O timeout não recebe duração ou tokens zero. Tokens usam os tokenizadores de cada fornecedor; saída reportada não é uma contagem de palavras nem uma fatura.

| Gerador | Condição | Requisito | Detectado | Vazio | Não detectado | Textos analisáveis |
|---|---|---|---:|---:|---:|---:|
| gemini | C0 | topic | 9 | 0 | 27 | 36 |
| gemini | C0 | grade_level | 35 | 0 | 1 | 36 |
| gemini | C0 | learning_objectives | 36 | 0 | 0 | 36 |
| gemini | C0 | duration_minutes | 34 | 0 | 2 | 36 |
| gemini | C0 | methodology | 6 | 0 | 30 | 36 |
| gemini | C0 | materials | 2 | 0 | 34 | 36 |
| gemini | C0 | assessment_strategy | 13 | 11 | 12 | 36 |
| gemini | C1 | topic | 14 | 0 | 21 | 35 |
| gemini | C1 | grade_level | 33 | 0 | 2 | 35 |
| gemini | C1 | learning_objectives | 34 | 0 | 1 | 35 |
| gemini | C1 | duration_minutes | 35 | 0 | 0 | 35 |
| gemini | C1 | methodology | 26 | 0 | 9 | 35 |
| gemini | C1 | materials | 27 | 3 | 5 | 35 |
| gemini | C1 | assessment_strategy | 15 | 9 | 11 | 35 |
| gemini | C2 | topic | 30 | 0 | 6 | 36 |
| gemini | C2 | grade_level | 18 | 0 | 18 | 36 |
| gemini | C2 | learning_objectives | 36 | 0 | 0 | 36 |
| gemini | C2 | duration_minutes | 36 | 0 | 0 | 36 |
| gemini | C2 | methodology | 35 | 0 | 1 | 36 |
| gemini | C2 | materials | 18 | 6 | 12 | 36 |
| gemini | C2 | assessment_strategy | 10 | 19 | 7 | 36 |
| qwen3 | C0 | topic | 10 | 0 | 26 | 36 |
| qwen3 | C0 | grade_level | 6 | 0 | 30 | 36 |
| qwen3 | C0 | learning_objectives | 34 | 0 | 2 | 36 |
| qwen3 | C0 | duration_minutes | 31 | 5 | 0 | 36 |
| qwen3 | C0 | methodology | 1 | 0 | 35 | 36 |
| qwen3 | C0 | materials | 5 | 0 | 31 | 36 |
| qwen3 | C0 | assessment_strategy | 28 | 7 | 1 | 36 |
| qwen3 | C1 | topic | 4 | 0 | 32 | 36 |
| qwen3 | C1 | grade_level | 36 | 0 | 0 | 36 |
| qwen3 | C1 | learning_objectives | 36 | 0 | 0 | 36 |
| qwen3 | C1 | duration_minutes | 36 | 0 | 0 | 36 |
| qwen3 | C1 | methodology | 31 | 0 | 5 | 36 |
| qwen3 | C1 | materials | 23 | 4 | 9 | 36 |
| qwen3 | C1 | assessment_strategy | 19 | 7 | 10 | 36 |
| qwen3 | C2 | topic | 26 | 0 | 10 | 36 |
| qwen3 | C2 | grade_level | 36 | 0 | 0 | 36 |
| qwen3 | C2 | learning_objectives | 31 | 5 | 0 | 36 |
| qwen3 | C2 | duration_minutes | 36 | 0 | 0 | 36 |
| qwen3 | C2 | methodology | 36 | 0 | 0 | 36 |
| qwen3 | C2 | materials | 35 | 0 | 1 | 36 |
| qwen3 | C2 | assessment_strategy | 33 | 3 | 0 | 36 |

## Duração numérica extraível

| Gerador | Condição | Declaração igual ao alvo | Diferente | Indeterminada | Divergência numérica detectada |
|---|---|---:|---:|---:|---:|
| gemini | C0 | 3 | 27 | 6 | 27 |
| gemini | C1 | 35 | 0 | 0 | 0 |
| gemini | C2 | 36 | 0 | 0 | 0 |
| qwen3 | C0 | 0 | 29 | 7 | 29 |
| qwen3 | C1 | 34 | 2 | 0 | 2 |
| qwen3 | C2 | 36 | 0 | 0 | 0 |

O extrator congelado reconhece declarações e intervalos HH:MM contíguos; não soma títulos arbitrários de etapas. Declaração de 50 minutos não demonstra cronograma consistente. Sem divergência detectada não se conclui consistência.

Os CSVs também separam cada uma das 12 tarefas. Não há teste de significância, score composto, avaliação factual ou conclusão de superioridade semântica de C2. C0 não recebeu seis requisitos-alvo; C1/C2 partilham o mesmo payload. Repetições e textos duplicados não são tarefas independentes.

O estado empty significa que as regras não associaram conteúdo ao rótulo reconhecido; não prova que a seção esteja realmente vazia. A detecção de campos requer padrões de rótulo previstos. Baixa detecção pode refletir formatação ou paráfrase. Esta etapa não recalibra o observador com as respostas principais. A estimativa semântica cabe à etapa posterior de julgamentos.

## Estimativa de custo Gemini

Estimativa bruta para as respostas com consumo reportado, usando a tabela congelada: US$ 0,75/milhão de entrada e US$ 3,75/milhão de saída, incluindo raciocínio. A saída faturável é inferida como total_tokens menos input_tokens. Não é fatura; não se presume desconto de cache. O custo do timeout é desconhecido e não recebe zero. Energia local não foi medida.

| Condição | Respostas com consumo disponível | Estimativa bruta USD |
|---|---:|---:|
| C0 | 36/36 | 0.21347325 |
| C1 | 35/36 | 0.17677425 |
| C2 | 36/36 | 0.16414350 |
