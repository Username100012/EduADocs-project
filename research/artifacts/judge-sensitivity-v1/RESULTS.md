# Sensibilidade da julgadora — casos sintéticos

36/36 julgamentos realizados; modelo `gpt-5.4-mini-2026-03-17`. Resultados separados do piloto de 81 julgamentos.

Três tarefas de Computação, quatro textos por tarefa e três julgamentos por texto. As versões-base são sintéticas e não foram presumidas perfeitas. A única linha retirada na omissão é o campo de materiais; a avaliação é substituída por capitais brasileiras no desalinhamento; na contradição temporal a prática passa de 20 para 70 minutos, elevando a soma de 50 para 100 enquanto a duração declarada permanece 50.

Relações e critério-alvo definidos antes das chamadas. Queda estrita é distinguida de empate e aumento; não se calcula uma nota geral nem se atribui zero a falhas.

| Tarefa | Alteração | Critério-alvo | Base | Variante | Diferença | Resultado |
|---|---|---|---:|---:|---:|---|
| pilot-001 | omission | semantic_fidelity | 4 | 4 | 0 | tie |
| pilot-001 | misalignment | instructional_alignment | 4 | 1 | -3 | decrease |
| pilot-001 | time_contradiction | coherence_feasibility | 4 | 1 | -3 | decrease |
| pilot-002 | omission | semantic_fidelity | 4 | 4 | 0 | tie |
| pilot-002 | misalignment | instructional_alignment | 4 | 1 | -3 | decrease |
| pilot-002 | time_contradiction | coherence_feasibility | 4 | 1 | -3 | decrease |
| pilot-003 | omission | semantic_fidelity | 4 | 4 | 0 | tie |
| pilot-003 | misalignment | instructional_alignment | 4 | 1 | -3 | decrease |
| pilot-003 | time_contradiction | coherence_feasibility | 4 | 1 | -3 | decrease |

Contagens: {"tie": 3, "decrease": 6}. Cada comparação usa a mediana dos três julgamentos, e as três alterações compartilham a mesma base em cada tarefa.

As notas dos quatro critérios para cada texto estão em `report.json`; prompts, candidatos, configuração, respostas brutas, justificativas e erros em `judgments.jsonl`.

## Justificativas nos casos de omissão

- `eval-c590547385e6e675c490edbfe7a5a023`, pilot-001, nota 4: A resposta contempla todos os elementos da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de produzir pseudocódigo e testes de mesa para casos presente/ausente.
- `eval-1fed07fa15a91ee38ee9b5e6f444d8b5`, pilot-003, nota 4: Repete os requisitos centrais da tarefa: tópico, nível, objetivos, duração, metodologia e a entrega de 2 requisitos funcionais e 2 não funcionais com justificativa e condição de verificação.
- `eval-1d98a601e2b506fc9e77b6e8bf004bcc`, pilot-003, nota 4: Repete os requisitos centrais da tarefa: tópico, nível, objetivos, metodologia, duração e a entrega de 2 requisitos funcionais e 2 não funcionais com justificativa e condição de verificação.
- `eval-8306d84e88b940b648fcc5ff45604fca`, pilot-002, nota 4: A resposta cobre todos os elementos da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de avaliação pedida ('duas consultas com SELECT e WHERE... e indicar os resultados esperados').
- `eval-31973b565ba4c3f4da17f0259357261b`, pilot-003, nota 4: Repete os requisitos centrais da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de avaliação com dois requisitos funcionais, dois não funcionais, justificativa e condição de verificação.
- `eval-baf95125b224981b6d7e52469771d74d`, pilot-001, nota 4: Repete todos os requisitos centrais da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de avaliação com pseudocódigo e testes de mesa para casos presente e ausente.
- `eval-78ce27e3ef5dec5658054b4700529677`, pilot-001, nota 4: Repete todos os elementos centrais da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de avaliação com pseudocódigo e testes de mesa para casos presente/ausente.
- `eval-56a573e6b82a27a8e805cf45fc975162`, pilot-002, nota 4: Repete os requisitos centrais da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de avaliação com duas consultas SELECT/WHERE e resultados esperados.
- `eval-111ea69c2a1f50eb6fd85a5efc25562f`, pilot-002, nota 4: A resposta contempla todos os requisitos da tarefa: tópico, nível, objetivos, duração, metodologia e a estratégia de avaliação com duas consultas SELECT/WHERE, uma por igualdade e outra por comparação numérica, além dos resultados esperados.

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

- omission (semantic_fidelity): 0/3 quedas, 3/3 empates.
- misalignment (instructional_alignment): 3/3 quedas, 0/3 empates.
- time_contradiction (coherence_feasibility): 3/3 quedas, 0/3 empates.

A retirada explícita dos materiais não provocou queda de fidelidade nas três tarefas. Isso impede apresentar a nota global de fidelidade como comprovação de cumprimento dos sete requisitos.

Antes da coleta principal, recomenda-se revisar de forma versionada a operacionalização da fidelidade, exigindo verificação e evidência por requisito. Não mudar os outros critérios ou ampliar a escala apenas para produzir diferenças C1/C2. Manter este piloto e este diagnóstico intactos; uma versão revisada precisa ser testada separadamente, inclusive com casos novos que não participaram do ajuste.
