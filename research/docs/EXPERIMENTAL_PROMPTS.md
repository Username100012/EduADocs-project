# Condições experimentais C0, C1 e C2

## Etapa 1 — Payload semântico comum

O experimento de plano de aula controla exatamente sete requisitos:

1. tópico;
2. nível educacional;
3. objetivo de aprendizagem;
4. duração;
5. metodologia;
6. materiais e recursos;
7. estratégia de avaliação.

Esses requisitos são representados por `LessonPlanSemanticPayload`, localizado em
`src/experiment/semantic_payload.py`.

O objeto é imutável, rejeita campos não declarados e só pode ser extraído de um plano de
aula que contenha os sete requisitos. Fluxo da aula, diferenciação, adaptações,
pré-requisitos e atividades de extensão não fazem parte desse objeto.

C1 e C2 deverão obrigatoriamente ser renderizados a partir da mesma instância do
payload. O método `canonical_json()` e a propriedade `semantic_hash` identificam a
informação controlada independentemente da organização textual do prompt.

## Etapa 2 — Condição C0

C0 é construída por `build_c0_prompt(topic)`. A assinatura aceita somente o tópico e o
tipo de material é fixado pelo template como plano de aula. Portanto, os demais seis
requisitos e os parâmetros operacionais não podem ser fornecidos ao construtor.

Template `lesson-plan-c0-generic-v1.0.0`:

```text
Elabore um plano de aula sobre o tema: {topic}.
```

O prompt não solicita formato, seções, nível educacional, objetivo, duração, metodologia,
materiais ou avaliação. Idioma também não é acrescentado como instrução nesta condição.

## Etapa 3 — Condição C1

C1 é construída por `build_c1_prompt(payload)` a partir de uma instância de
`LessonPlanSemanticPayload`. Os sete requisitos são apresentados em um único parágrafo
de linguagem natural, sem listas, rótulos de campos, títulos ou regras de formatação.

Template `lesson-plan-c1-free-text-v1.0.0`:

```text
Elabore um plano de aula sobre {topic} para estudantes do nível {grade_level}, com
duração de {duration_minutes} minutos. O objetivo de aprendizagem é
{learning_objectives}. Utilize {methodology} como metodologia, considerando {materials}
como materiais e recursos disponíveis e {assessment_strategy} como estratégia de
avaliação.
```

O construtor aceita somente o payload semântico. Assim, parâmetros operacionais não
podem ser acrescentados pela interface dessa função.

## Etapa 4 — Condição C2

C2 é construída por `build_c2_prompt(payload)` e recebe o mesmo tipo de objeto semântico
usado por C1. A diferença está na organização explícita da instrução em três blocos:

- tarefa;
- parâmetros pedagógicos;
- instrução de saída.

Template `lesson-plan-c2-structured-v1.0.0`:

```text
TAREFA
Elaborar um plano de aula.

PARÂMETROS PEDAGÓGICOS
- Tópico: {topic}
- Nível educacional: {grade_level}
- Objetivo de aprendizagem: {learning_objectives}
- Duração: {duration_minutes} minutos
- Metodologia: {methodology}
- Materiais e recursos: {materials}
- Estratégia de avaliação: {assessment_strategy}

INSTRUÇÃO DE SAÍDA
Produza o plano de aula respeitando todos os parâmetros pedagógicos apresentados.
```

Nenhuma seção pedagógica adicional foi solicitada. A próxima etapa deverá demonstrar,
por testes próprios, que C1 e C2 preservam o mesmo conteúdo informacional e diferem na
estrutura textual.

## Etapa 5 — Equivalência informacional C1–C2

Os artefatos de C1 e C2 registram `semantic_payload_hash`, calculado sobre a
serialização canônica dos sete requisitos. Para uma mesma tarefa:

```text
C1.semantic_payload_hash = C2.semantic_payload_hash
C1.sha256 != C2.sha256
```

A primeira relação demonstra que ambos derivam do mesmo conteúdo controlado. A segunda
confirma que os prompts possuem representações textuais diferentes. Testes adicionais
verificam que os mesmos sete valores aparecem exatamente uma vez em cada condição, que
C1 permanece em um parágrafo, que C2 contém blocos e rótulos explícitos e que nenhuma
das duas condições incorpora parâmetros operacionais.

## Etapa 6 — Pacote de prompts de uma tarefa

`ExperimentalTaskPromptSet` representa uma tarefa experimental antes de qualquer chamada
a modelos. Ele reúne:

- identificador da tarefa;
- payload semântico com os sete requisitos;
- prompt C0;
- prompt C1;
- prompt C2.

O objeto valida versões, requisitos esperados, proveniência semântica de C1/C2 e diferença
estrutural entre essas condições. `to_manifest_dict()` fornece uma representação com os
textos, versões e hashes que poderá ser incorporada ao manifesto do experimento.

Esse componente apenas empacota e valida prompts. Ele não seleciona modelos, não executa
chamadas, não cria repetições e não consome tokens.

## Etapa 7 — Esquema do catálogo de tarefas

`ExperimentalTaskCatalog` define o arquivo que armazenará as tarefas do estudo. A versão
inicial exige exatamente 12 tarefas, idioma `pt-BR`, identificadores no padrão
`task-NNN`, áreas ou disciplinas informadas e payloads semânticos únicos.

O catálogo possui serialização canônica e `catalog_hash`. Ele pode ser salvo e carregado
em JSON e pode construir os 12 pacotes C0/C1/C2 sem executar modelos. O esquema JSON
correspondente encontra-se em `experiments/task_catalog.schema.json`.

O conteúdo definitivo das 12 tarefas ainda não foi criado. A seleção desses conteúdos é
uma decisão metodológica posterior e não deve ser preenchida automaticamente.

## Etapa 8 — Rubrica computacional

A especificação das métricas foi congelada antes da criação das tarefas em
`experiments/computational_rubric.v1.json`. A justificativa, as regras de pontuação, o
tratamento de falhas, as métricas secundárias, a análise estatística e os limites das
conclusões estão documentados em `docs/COMPUTATIONAL_EVALUATION_RUBRIC.md`.

Esta etapa define o protocolo, mas ainda não implementa os validadores que atribuirão as
pontuações 0, 0,5 e 1.
