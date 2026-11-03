# Indicadores computacionais principais — v2

Análise das respostas reais salvas, sem novas chamadas.

Resultados de extração textual e operação. Não são notas de qualidade ou taxas comprovadas de atendimento semântico. Os estados são contados sobre todos os textos analisáveis, mantendo indeterminados no denominador.

| Gerador | Condição | Planejadas | Iniciadas | Concluídas | Textos analisáveis | Latência mediana ms | IQR ms |
|---|---|---:|---:|---:|---:|---:|---:|
| qwen3 | C0 | 9 | 9 | 9 | 9 | 22451.156099996297 | 652.7058000065153 |
| qwen3 | C1 | 9 | 9 | 9 | 9 | 28106.052200004342 | 3664.2231000005268 |
| qwen3 | C2 | 9 | 9 | 9 | 9 | 23471.031099994434 | 1055.1963000034448 |

| Gerador | Condição | Requisito | Correspondência | Não correspondência | Indeterminado | Denominador |
|---|---|---|---:|---:|---:|---:|
| qwen3 | C0 | topic | 9 | 0 | 0 | 9 |
| qwen3 | C0 | grade_level | 9 | 0 | 0 | 9 |
| qwen3 | C0 | learning_objectives | 6 | 3 | 0 | 9 |
| qwen3 | C0 | duration_minutes | 0 | 9 | 0 | 9 |
| qwen3 | C0 | methodology | 0 | 0 | 9 | 9 |
| qwen3 | C0 | materials | 0 | 1 | 8 | 9 |
| qwen3 | C0 | assessment_strategy | 0 | 9 | 0 | 9 |
| qwen3 | C1 | topic | 9 | 0 | 0 | 9 |
| qwen3 | C1 | grade_level | 9 | 0 | 0 | 9 |
| qwen3 | C1 | learning_objectives | 9 | 0 | 0 | 9 |
| qwen3 | C1 | duration_minutes | 9 | 0 | 0 | 9 |
| qwen3 | C1 | methodology | 5 | 1 | 3 | 9 |
| qwen3 | C1 | materials | 4 | 0 | 5 | 9 |
| qwen3 | C1 | assessment_strategy | 4 | 2 | 3 | 9 |
| qwen3 | C2 | topic | 9 | 0 | 0 | 9 |
| qwen3 | C2 | grade_level | 9 | 0 | 0 | 9 |
| qwen3 | C2 | learning_objectives | 9 | 0 | 0 | 9 |
| qwen3 | C2 | duration_minutes | 9 | 0 | 0 | 9 |
| qwen3 | C2 | methodology | 4 | 0 | 5 | 9 |
| qwen3 | C2 | materials | 7 | 0 | 2 | 9 |
| qwen3 | C2 | assessment_strategy | 6 | 3 | 0 | 9 |

O JSON também separa tarefas, estados de término, cobertura de tokens e contagem de palavras. IQR usa quartis inclusivos; com menos de duas medidas permanece nulo. Tempos incluem efeitos de rede/carregamento. C0 não recebeu os seis requisitos além do tópico. Não há score composto, falhas com nota zero, testes de significância ou nova chamada à API.
