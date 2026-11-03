# Coleta principal concluída — eduadocs-main-v1.0.0

Execução real iniciada em 26/10/2026, separada do piloto.

**216/216 tentativas registradas: 215 planos gerados com sucesso e 1 falha(s).**

| Gerador | Condição | Tentativas | Sucessos | Falhas |
|---|---|---:|---:|---:|
| gemini | C0 | 36 | 36 | 0 |
| gemini | C1 | 36 | 35 | 1 |
| gemini | C2 | 36 | 36 | 0 |
| qwen3 | C0 | 36 | 36 | 0 |
| qwen3 | C1 | 36 | 36 | 0 |
| qwen3 | C2 | 36 | 36 | 0 |

## Integridade

Todos os 216 IDs planejados têm exatamente um início e um resultado, sem chamadas pendentes. Cada célula gerador/condição teve 36 tentativas. O protocolo, os prompts e os artefatos selados permaneceram inalterados; o piloto não foi sobrescrito.

O primeiro processo encerrou após 47 tentativas, com 46 sucessos e um ReadTimeout do Gemini. Após conferir o selo e ausência de chamada pendente, retomou-se o mesmo comando para os 169 IDs ainda não executados. Nenhum ID concluído, inclusive a falha, foi repetido. A falha permanece no log:
- `gemini:task-002:c1:r1`: `ReadTimeout`.

As 215 respostas elegíveis poderão receber até 645 julgamentos. Nenhum julgamento GPT foi executado nesta etapa. Sucesso de geração é técnico, não validação da qualidade do material.

Dados originais: `generations.jsonl`. Resumo auditável: `collection_summary.json`. [Protocolo congelado](../../docs/MAIN_STUDY_PROTOCOL.md).

SHA-256 do log final: `70969e6fe4df45f92d7dd9605eb68cb90b6dfa9eaa6d0346bb2f1f1a4b5b4135`.

## Indicadores automáticos concluídos

[Relatório local](AUTOMATIC_METRICS.md), `automatic_summary.v1.json` e CSVs de campos, duração e operação. A análise mantém o timeout separado e preserva os textos originais. [Método e limites observados](../../docs/MAIN_AUTOMATIC_ANALYSIS_2026-10-26.md). Nenhuma chamada às APIs nesta etapa; julgamentos GPT ainda não executados.

## Fila de julgamentos preparada

[645 julgamentos conferidos offline](../main-judgments-v1/README.md), três por plano elegível. Timeout excluído sem reposição. Nenhum julgamento GPT foi executado na preparação.
