# Julgamentos semânticos do piloto local

Modelo: `gpt-5.4-mini-2026-03-17`. Concluídos 81/81 julgamentos; 81 válidos. O teste técnico prévio não entra neste lote.

Escala ordinal de 1 a 4. Primeiro é calculada a mediana de três julgamentos de cada resposta; depois, a mediana dessas medianas por condição. Intervalos abaixo são mínimo–máximo entre medianas das respostas, não intervalos de confiança.

| Critério | C0 | C1 | C2 |
|---|---|---|---|
| Fidelidade à tarefa | 2 [2–2], n=9 | 4 [4–4], n=9 | 4 [3–4], n=9 |
| Alinhamento interno | 2 [2–2], n=9 | 4 [4–4], n=9 | 4 [4–4], n=9 |
| Adequação ao nível | 2 [2–3], n=9 | 4 [3–4], n=9 | 4 [4–4], n=9 |
| Coerência e exequibilidade | 3 [2–3], n=9 | 4 [3–4], n=9 | 4 [3–4], n=9 |

## Por tarefa e condição

| Tarefa | Condição | Critério | Mediana | Mín.–máx. | Trincas em concordância exata |
|---|---|---|---:|---|---|
| pilot-001 | C0 | Fidelidade à tarefa | 2 | 2–2 | 3/3 |
| pilot-001 | C0 | Alinhamento interno | 2 | 2–2 | 3/3 |
| pilot-001 | C0 | Adequação ao nível | 3 | 2–3 | 1/3 |
| pilot-001 | C0 | Coerência e exequibilidade | 3 | 3–3 | 3/3 |
| pilot-001 | C1 | Fidelidade à tarefa | 4 | 4–4 | 3/3 |
| pilot-001 | C1 | Alinhamento interno | 4 | 4–4 | 3/3 |
| pilot-001 | C1 | Adequação ao nível | 4 | 3–4 | 3/3 |
| pilot-001 | C1 | Coerência e exequibilidade | 4 | 3–4 | 3/3 |
| pilot-001 | C2 | Fidelidade à tarefa | 4 | 3–4 | 1/3 |
| pilot-001 | C2 | Alinhamento interno | 4 | 4–4 | 3/3 |
| pilot-001 | C2 | Adequação ao nível | 4 | 4–4 | 3/3 |
| pilot-001 | C2 | Coerência e exequibilidade | 3 | 3–3 | 2/3 |
| pilot-002 | C0 | Fidelidade à tarefa | 2 | 2–2 | 3/3 |
| pilot-002 | C0 | Alinhamento interno | 2 | 2–2 | 3/3 |
| pilot-002 | C0 | Adequação ao nível | 2 | 2–3 | 3/3 |
| pilot-002 | C0 | Coerência e exequibilidade | 2 | 2–3 | 3/3 |
| pilot-002 | C1 | Fidelidade à tarefa | 4 | 4–4 | 3/3 |
| pilot-002 | C1 | Alinhamento interno | 4 | 4–4 | 3/3 |
| pilot-002 | C1 | Adequação ao nível | 4 | 4–4 | 3/3 |
| pilot-002 | C1 | Coerência e exequibilidade | 4 | 4–4 | 3/3 |
| pilot-002 | C2 | Fidelidade à tarefa | 4 | 4–4 | 3/3 |
| pilot-002 | C2 | Alinhamento interno | 4 | 4–4 | 3/3 |
| pilot-002 | C2 | Adequação ao nível | 4 | 4–4 | 3/3 |
| pilot-002 | C2 | Coerência e exequibilidade | 4 | 4–4 | 3/3 |
| pilot-003 | C0 | Fidelidade à tarefa | 2 | 2–2 | 3/3 |
| pilot-003 | C0 | Alinhamento interno | 2 | 2–2 | 3/3 |
| pilot-003 | C0 | Adequação ao nível | 2 | 2–3 | 1/3 |
| pilot-003 | C0 | Coerência e exequibilidade | 2 | 2–3 | 0/3 |
| pilot-003 | C1 | Fidelidade à tarefa | 4 | 4–4 | 3/3 |
| pilot-003 | C1 | Alinhamento interno | 4 | 4–4 | 3/3 |
| pilot-003 | C1 | Adequação ao nível | 4 | 4–4 | 3/3 |
| pilot-003 | C1 | Coerência e exequibilidade | 4 | 4–4 | 3/3 |
| pilot-003 | C2 | Fidelidade à tarefa | 4 | 4–4 | 3/3 |
| pilot-003 | C2 | Alinhamento interno | 4 | 4–4 | 3/3 |
| pilot-003 | C2 | Adequação ao nível | 4 | 4–4 | 3/3 |
| pilot-003 | C2 | Coerência e exequibilidade | 4 | 3–4 | 2/3 |

## Uso e limites

Concordância exata: 97/108 trincas por resposta/critério. Amplitude máxima dentro de uma trinca: 1 ponto(s). Concordância não comprova validade das notas.

Tokens de entrada: 175884; saída: 22794; entrada em cache: 56960. Soma das latências: 197.47 s. O custo monetário não foi presumido.

- Judge scores are automated estimates, not human or pedagogical validation.
- No factual correctness or learning efficacy claims.
- C0 did not receive the six requirements beyond topic.
- Fixed-seed generation repetitions and judge repetitions are not independent samples.
- Only complete three-judgment sets enter response medians; failures are not scored zero.
- No composite score, significance tests or cloud-generator comparison.

As justificativas e as 324 notas individuais previstas ficam em `judgment_scores.csv`; as medianas por plano em `judgment_response_medians.csv`; respostas brutas, prompts, configuração e erros em `judgments.jsonl`. O resumo deve ser lido junto da análise lexical v2. Diferenças descritivas não estabelecem superioridade geral de uma condição.
