# Comparação de sensibilidade — Mini e Sol

36 julgamentos válidos por configuração. Verificados textos, payloads, prompts, IDs, rubrica e esquema idênticos. Os resultados do piloto de 81 julgamentos não foram recalculados.

## Comparação por defeito

| Alteração | Mini: quedas/3 | Sol: quedas/3 | Mini: empates/3 | Sol: empates/3 |
|---|---:|---:|---:|---:|
| omission | 0 | 3 | 3 | 0 |
| misalignment | 3 | 3 | 0 | 0 |
| time_contradiction | 3 | 3 | 0 | 0 |

## Medianas por tarefa

| Tarefa | Alteração | Mini: base → variante | Sol: base → variante |
|---|---|---|---|
| pilot-001 | omission | 4 → 4 | 4 → 3 |
| pilot-001 | misalignment | 4 → 1 | 4 → 2 |
| pilot-001 | time_contradiction | 4 → 1 | 4 → 2 |
| pilot-002 | omission | 4 → 4 | 4 → 3 |
| pilot-002 | misalignment | 4 → 1 | 4 → 2 |
| pilot-002 | time_contradiction | 4 → 1 | 4 → 2 |
| pilot-003 | omission | 4 → 4 | 4 → 3 |
| pilot-003 | misalignment | 4 → 1 | 4 → 2 |
| pilot-003 | time_contradiction | 4 → 1 | 4 → 2 |

## Consumo e estabilidade

| Modelo | Entrada | Saída | Latência mediana (s) | Estimativa US$ | Trincas com concordância exata |
|---|---:|---:|---:|---:|---:|
| gpt-5.4-mini-2026-03-17 | 42766 | 10051 | 2.30 | 0.0773 | 40/48 |
| gpt-6.1-sol | 42766 | 11580 | 7.99 | 0.2227 | 44/48 |

Estimativas segundo [preços oficiais](https://developers.openai.com/api/docs/pricing), consultados em 19/10/2026. O JSON registra cache de leitura/escrita e tokens de raciocínio. A chamada técnica Sol fica fora das 36 e desses custos.

## Interpretação

Sol uses reasoning low, omits temperature/top_p, and caps output at 4096 including reasoning; Mini used none, temperature 0, top_p 1, cap 1200. Not a pure model-only causal comparison.

Sol's published model identifier has no dated snapshot in the consulted model page. Preserve returned metadata; do not claim immutable version.

- Three synthetic pilot-domain tasks and deliberately obvious defects; exploratory, not independent validation.
- Shared controls and repetitions are dependent; no significance tests or overall quality score.
- Choosing a model after these tests requires checking reserved cases before the main study.

O Sol penalizou a omissão explícita de materiais nas três tarefas, enquanto o Mini empatou com as bases. Isso favorece o Sol neste diagnóstico específico, mas não o valida como juiz geral. Antes de adotá-lo na coleta principal, verificar sensibilidade em casos reservados e registrar definitivamente a configuração. Não substituir retroativamente os julgamentos antigos.
