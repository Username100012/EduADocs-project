# Resultado do piloto local Qwen3

Execução real de 27 gerações: três tarefas × três condições × três repetições. Nenhuma chamada Google ou OpenAI. Os pesos e a versão do Ollama foram conferidos pelo executor antes da coleta.

- Concluídas normalmente: 27/27.
- Falhas técnicas ou truncamentos: 0.
- Soma das latências das chamadas: 683.5 segundos (inclui carregamento quando existente; não é tempo exclusivo de inferência).

| Condição | Respostas | Latência mediana (s) | Divergências de duração detectadas contra o alvo |
|---|---:|---:|---:|
| C0 | 9 | 22.45 | 6 |
| C1 | 9 | 28.11 | 0 |
| C2 | 9 | 23.47 | 0 |

O campo técnico `detected_contradiction` inclui divergência entre duração declarada e alvo de 50 minutos, além de contradições extraíveis. C0 não recebe a duração-alvo; portanto esses casos não comprovam inconsistência interna nem desobediência a uma instrução recebida. Zero detecções em C1/C2 não comprova atendimento integral: o extrator pode não reconhecer durações ou cronogramas.

## Estabilidade com seed fixa

| Tarefa | Condição | Textos distintos nas três repetições (hash do texto) |
|---|---|---:|
| pilot-001 | C0 | 3 |
| pilot-001 | C1 | 3 |
| pilot-001 | C2 | 1 |
| pilot-002 | C0 | 2 |
| pilot-002 | C1 | 2 |
| pilot-002 | C2 | 2 |
| pilot-003 | C0 | 1 |
| pilot-003 | C1 | 2 |
| pilot-003 | C2 | 2 |

Há repetições idênticas e distintas. Seed fixa não garantiu identidade completa, e as repetições não são tratadas como amostras independentes.

## Artefatos e interpretação

- `generations.jsonl`: configuração original, plano selecionado, prompts, identificadores, respostas e metadados.
- `automatic_metrics.json`: métricas por resposta, evidências textuais e hashes da origem.
- `responses/`: cópias dos textos em Markdown para inspeção, sem alterar os originais.

As métricas lexicais são proxies operacionais; não demonstram qualidade pedagógica, correção factual ou superioridade de C2. A comparação com Gemini e a estimativa semântica da julgadora permanecem pendentes. A configuração original do piloto não foi alterada.

Próxima etapa: auditar as extrações e sintetizar os sete requisitos por tarefa e condição, incluindo casos sem extração; não regenerar as respostas em função dos resultados.
