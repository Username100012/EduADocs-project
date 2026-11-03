# Sensibilidade da julgadora — casos sintéticos

36/36 julgamentos realizados; modelo `gpt-6.1-sol`. Resultados separados do piloto de 81 julgamentos.

Três tarefas de Computação, quatro textos por tarefa e três julgamentos por texto. As versões-base são sintéticas e não foram presumidas perfeitas. A única linha retirada na omissão é o campo de materiais; a avaliação é substituída por capitais brasileiras no desalinhamento; na contradição temporal a prática passa de 20 para 70 minutos, elevando a soma de 50 para 100 enquanto a duração declarada permanece 50.

Relações e critério-alvo definidos antes das chamadas. Queda estrita é distinguida de empate e aumento; não se calcula uma nota geral nem se atribui zero a falhas.

| Tarefa | Alteração | Critério-alvo | Base | Variante | Diferença | Resultado |
|---|---|---|---:|---:|---:|---|
| pilot-001 | omission | semantic_fidelity | 4 | 3 | -1 | decrease |
| pilot-001 | misalignment | instructional_alignment | 4 | 2 | -2 | decrease |
| pilot-001 | time_contradiction | coherence_feasibility | 4 | 2 | -2 | decrease |
| pilot-002 | omission | semantic_fidelity | 4 | 3 | -1 | decrease |
| pilot-002 | misalignment | instructional_alignment | 4 | 2 | -2 | decrease |
| pilot-002 | time_contradiction | coherence_feasibility | 4 | 2 | -2 | decrease |
| pilot-003 | omission | semantic_fidelity | 4 | 3 | -1 | decrease |
| pilot-003 | misalignment | instructional_alignment | 4 | 2 | -2 | decrease |
| pilot-003 | time_contradiction | coherence_feasibility | 4 | 2 | -2 | decrease |

Contagens: {"decrease": 9}. Cada comparação usa a mediana dos três julgamentos, e as três alterações compartilham a mesma base em cada tarefa.

As notas dos quatro critérios para cada texto estão em `report.json`; prompts, candidatos, configuração, respostas brutas, justificativas e erros em `judgments.jsonl`.

## Justificativas nos casos de omissão

- `eval-c590547385e6e675c490edbfe7a5a023`, pilot-001, nota 3: Contempla tema, nível, objetivos, duração, colaboração e avaliação solicitados, mas omite o quadro e a folha com vetores previstos nos materiais.
- `eval-1fed07fa15a91ee38ee9b5e6f444d8b5`, pilot-003, nota 3: Preserva tema, nível, objetivos, metodologia, avaliação e duração de 50 minutos, mas não menciona o quadro nem a folha com a descrição do sistema de empréstimos.
- `eval-1d98a601e2b506fc9e77b6e8bf004bcc`, pilot-003, nota 3: Preserva tema, nível, objetivos, metodologia, duração e entrega avaliativa, mas omite o quadro e a folha com a descrição do sistema previstos na tarefa.
- `eval-8306d84e88b940b648fcc5ff45604fca`, pilot-002, nota 3: Preserva tema, nível, objetivos, metodologia, duração e avaliação, mas omite o quadro e a folha com tabela de produtos contendo código, nome e preço.
- `eval-31973b565ba4c3f4da17f0259357261b`, pilot-003, nota 3: Preserva tema, nível, objetivos, metodologia, duração e avaliação solicitados, mas não menciona o quadro nem a folha com a descrição do sistema.
- `eval-baf95125b224981b6d7e52469771d74d`, pilot-001, nota 3: Contempla tema, nível, objetivos, metodologia, duração e avaliação solicitados, mas omite o quadro e a folha com vetores previstos como materiais.
- `eval-78ce27e3ef5dec5658054b4700529677`, pilot-001, nota 3: Contempla tema, nível, objetivos, duração, metodologia e avaliação solicitados, mas omite os materiais previstos: quadro e folha com vetores de inteiros.
- `eval-56a573e6b82a27a8e805cf45fc975162`, pilot-002, nota 3: Preserva tema, nível, objetivos, metodologia, duração e avaliação solicitados, mas omite o quadro e a folha com tabela contendo código, nome e preço.
- `eval-111ea69c2a1f50eb6fd85a5efc25562f`, pilot-002, nota 3: Preserva tema, nível, objetivos, metodologia, duração e avaliação solicitados, mas omite o quadro e a folha com tabela de produtos contendo código, nome e preço.

## Limites

- Constructed perturbations are diagnostic expectations, not validated gold-standard scores.
- Three synthetic tasks reuse pilot target payloads; no independent generalization validation.
- Shared baseline for three variants; comparisons and repeated judgments are dependent.
- A tie is not strict defect sensitivity. Baseline is not assumed to deserve score 4.
- No factual, human or pedagogical efficacy validation; no significance tests or rubric changes.
- A generic resource reference can remain implicit after removal of the explicit materials field.
- No claim of complete defect isolation across semantic criteria; inspect all four scores.

Interpretação: quedas demonstram resposta às alterações neste conjunto limitado; não estabelecem confiabilidade geral. Empates ou aumentos exigem examinar o contexto e as justificativas antes de revisar a rubrica. O piloto original permanece preservado.

## Resultado observado e decisão

- omission (semantic_fidelity): 3/3 quedas, 0/3 empates.
- misalignment (instructional_alignment): 3/3 quedas, 0/3 empates.
- time_contradiction (coherence_feasibility): 3/3 quedas, 0/3 empates.