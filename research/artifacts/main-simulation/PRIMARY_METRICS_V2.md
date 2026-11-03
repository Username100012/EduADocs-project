# Indicadores computacionais principais — v2

SIMULAÇÃO: respostas fictícias, sem valor experimental.

Resultados de extração textual e operação. Não são notas de qualidade ou taxas comprovadas de atendimento semântico. Os estados são contados sobre todos os textos analisáveis, mantendo indeterminados no denominador.

| Gerador | Condição | Planejadas | Iniciadas | Concluídas | Textos analisáveis | Latência mediana ms | IQR ms |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini | C0 | 36 | 36 | 36 | 36 | 0.0 | 0.0 |
| gemini | C1 | 36 | 36 | 36 | 36 | 0.0 | 0.0 |
| gemini | C2 | 36 | 36 | 36 | 36 | 0.0 | 0.0 |
| qwen3 | C0 | 36 | 36 | 36 | 36 | 0.0 | 0.0 |
| qwen3 | C1 | 36 | 36 | 36 | 36 | 0.0 | 0.0 |
| qwen3 | C2 | 36 | 36 | 36 | 36 | 0.0 | 0.0 |

| Gerador | Condição | Requisito | Correspondência | Não correspondência | Indeterminado | Denominador |
|---|---|---|---:|---:|---:|---:|
| gemini | C0 | topic | 0 | 36 | 0 | 36 |
| gemini | C0 | grade_level | 0 | 36 | 0 | 36 |
| gemini | C0 | learning_objectives | 0 | 0 | 36 | 36 |
| gemini | C0 | duration_minutes | 0 | 0 | 36 | 36 |
| gemini | C0 | methodology | 0 | 0 | 36 | 36 |
| gemini | C0 | materials | 0 | 0 | 36 | 36 |
| gemini | C0 | assessment_strategy | 0 | 0 | 36 | 36 |
| gemini | C1 | topic | 0 | 36 | 0 | 36 |
| gemini | C1 | grade_level | 0 | 36 | 0 | 36 |
| gemini | C1 | learning_objectives | 0 | 0 | 36 | 36 |
| gemini | C1 | duration_minutes | 0 | 0 | 36 | 36 |
| gemini | C1 | methodology | 0 | 0 | 36 | 36 |
| gemini | C1 | materials | 0 | 0 | 36 | 36 |
| gemini | C1 | assessment_strategy | 0 | 0 | 36 | 36 |
| gemini | C2 | topic | 0 | 36 | 0 | 36 |
| gemini | C2 | grade_level | 0 | 36 | 0 | 36 |
| gemini | C2 | learning_objectives | 0 | 0 | 36 | 36 |
| gemini | C2 | duration_minutes | 0 | 0 | 36 | 36 |
| gemini | C2 | methodology | 0 | 0 | 36 | 36 |
| gemini | C2 | materials | 0 | 0 | 36 | 36 |
| gemini | C2 | assessment_strategy | 0 | 0 | 36 | 36 |
| qwen3 | C0 | topic | 0 | 36 | 0 | 36 |
| qwen3 | C0 | grade_level | 0 | 36 | 0 | 36 |
| qwen3 | C0 | learning_objectives | 0 | 0 | 36 | 36 |
| qwen3 | C0 | duration_minutes | 0 | 0 | 36 | 36 |
| qwen3 | C0 | methodology | 0 | 0 | 36 | 36 |
| qwen3 | C0 | materials | 0 | 0 | 36 | 36 |
| qwen3 | C0 | assessment_strategy | 0 | 0 | 36 | 36 |
| qwen3 | C1 | topic | 0 | 36 | 0 | 36 |
| qwen3 | C1 | grade_level | 0 | 36 | 0 | 36 |
| qwen3 | C1 | learning_objectives | 0 | 0 | 36 | 36 |
| qwen3 | C1 | duration_minutes | 0 | 0 | 36 | 36 |
| qwen3 | C1 | methodology | 0 | 0 | 36 | 36 |
| qwen3 | C1 | materials | 0 | 0 | 36 | 36 |
| qwen3 | C1 | assessment_strategy | 0 | 0 | 36 | 36 |
| qwen3 | C2 | topic | 0 | 36 | 0 | 36 |
| qwen3 | C2 | grade_level | 0 | 36 | 0 | 36 |
| qwen3 | C2 | learning_objectives | 0 | 0 | 36 | 36 |
| qwen3 | C2 | duration_minutes | 0 | 0 | 36 | 36 |
| qwen3 | C2 | methodology | 0 | 0 | 36 | 36 |
| qwen3 | C2 | materials | 0 | 0 | 36 | 36 |
| qwen3 | C2 | assessment_strategy | 0 | 0 | 36 | 36 |

O JSON também separa tarefas, estados de término, cobertura de tokens e contagem de palavras. IQR usa quartis inclusivos; com menos de duas medidas permanece nulo. Tempos incluem efeitos de rede/carregamento. C0 não recebeu os seis requisitos além do tópico. Não há score composto, falhas com nota zero, testes de significância ou nova chamada à API.
