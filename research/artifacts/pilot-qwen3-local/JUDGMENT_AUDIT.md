# Auditoria offline da julgadora

324 notas de 81 julgamentos, sobre 27 planos. Nenhuma nova chamada à API; notas, justificativas e arquivos anteriores preservados.

## Distribuições e concentração no teto

As contagens são de notas individuais, não de amostras independentes. Cada resposta foi julgada três vezes.

| Condição | Critério | Nota 1 | Nota 2 | Nota 3 | Nota 4 | % de nota máxima |
|---|---|---:|---:|---:|---:|---:|
| C0 | Fidelidade à tarefa | 0 | 27 | 0 | 0 | 0.0% |
| C0 | Alinhamento interno | 0 | 27 | 0 | 0 | 0.0% |
| C0 | Adequação ao nível | 0 | 15 | 12 | 0 | 0.0% |
| C0 | Coerência e exequibilidade | 0 | 11 | 16 | 0 | 0.0% |
| C1 | Fidelidade à tarefa | 0 | 0 | 0 | 27 | 100.0% |
| C1 | Alinhamento interno | 0 | 0 | 0 | 27 | 100.0% |
| C1 | Adequação ao nível | 0 | 0 | 3 | 24 | 88.9% |
| C1 | Coerência e exequibilidade | 0 | 0 | 3 | 24 | 88.9% |
| C2 | Fidelidade à tarefa | 0 | 0 | 5 | 22 | 81.5% |
| C2 | Alinhamento interno | 0 | 0 | 0 | 27 | 100.0% |
| C2 | Adequação ao nível | 0 | 0 | 0 | 27 | 100.0% |
| C2 | Coerência e exequibilidade | 0 | 1 | 10 | 16 | 59.3% |

## C1 versus C2 por tarefa

Mediana das três medianas por resposta em cada tarefa. Não há pareamento artificial por índice de repetição.

| Tarefa | Critério | C1 | C2 | C2 − C1 |
|---|---|---:|---:|---:|
| pilot-001 | Fidelidade à tarefa | 4 | 4 | 0 |
| pilot-001 | Alinhamento interno | 4 | 4 | 0 |
| pilot-001 | Adequação ao nível | 4 | 4 | 0 |
| pilot-001 | Coerência e exequibilidade | 4 | 3 | -1 |
| pilot-002 | Fidelidade à tarefa | 4 | 4 | 0 |
| pilot-002 | Alinhamento interno | 4 | 4 | 0 |
| pilot-002 | Adequação ao nível | 4 | 4 | 0 |
| pilot-002 | Coerência e exequibilidade | 4 | 4 | 0 |
| pilot-003 | Fidelidade à tarefa | 4 | 4 | 0 |
| pilot-003 | Alinhamento interno | 4 | 4 | 0 |
| pilot-003 | Adequação ao nível | 4 | 4 | 0 |
| pilot-003 | Coerência e exequibilidade | 4 | 4 | 0 |

## Justificativas: achados e limites

Foram detectadas 1 alegações aritméticas falsas no padrão verificável. O teste não cobre todas as possíveis falhas de justificativa.

- `eval-a21206d625ea52d5ba01de0f2ddd5476`, `qwen3:pilot-003:c2:r3`, Coerência e exequibilidade, nota 3: O plano é executável e coerente, mas há pequena inconsistência temporal: a soma das etapas (5+35+10) excede a duração declarada de 50 minutos.
  Verificação: 5+35+10 = 50, duração declarada 50. A afirmação de excesso é falsa; isso não prova que toda a nota deva ser outra.
  Fonte, linha 10: - **Duração:** 50 minutos
  Fonte, linha 27: #### **I. Introdução (5 minutos)**
  Fonte, linha 37: #### **II. Atividade Principal (35 minutos)**
  Fonte, linha 58: #### **III. Conclusão e Refletir (10 minutos)**

Há 0 justificativas de nota máxima sinalizadas por palavras de ressalva; são candidatas, não contradições confirmadas. Há 22 notas abaixo de 4 em C1/C2, todas preservadas no JSON da auditoria.

Há 3 grupos de texto idêntico/critério com medianas diferentes entre avaliações. Isso expõe variabilidade da julgadora mesmo sem mudança no conteúdo; as respostas repetidas não são independentes.

## Decisão metodológica

Existe forte concentração em notas máximas em C1/C2. Ela limita a discriminação neste recorte, sem provar que a rubrica seja inválida ou que as condições sejam equivalentes. Não se recomenda ampliar a escala, alterar âncoras ou trocar a julgadora apenas para produzir diferenças entre C1 e C2.

O erro aritmético demonstrado impede tratar as justificativas como verdade de referência. A concordância elevada não substitui validação; problemas reais podem ser ignorados ou penalidades podem apoiar-se em afirmações erradas. As notas devem permanecer como estimativa secundária, acompanhadas das métricas computacionais e casos de falha.

Próximo passo recomendado: executar testes de sensibilidade com casos sintéticos de defeitos conhecidos (omissão, desalinhamento e contradição temporal), usando os casos metamórficos já definidos. Registrar os resultados separadamente; qualquer revisão posterior deve ser versionada e avaliada em casos não usados no ajuste. Não editar nem substituir as notas deste piloto.

A auditoria é computacional e exploratória, sem participantes humanos. Não houve avaliação externa de correção factual ou de eficácia pedagógica. C0 é avaliada contra seis requisitos não informados, de modo que sua diferença não isola estrutura de prompt.
