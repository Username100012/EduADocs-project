# Mensuração dos requisitos e contrato da julgadora v2

Especificação fechada para implementação local em 19/10/2026. Ainda não validada empiricamente com a API ou como instrumento semântico. Sem novas chamadas e sem substituição das notas anteriores.

## Duas medidas distintas

**Observação computacional:** `detected`, `empty` ou `not_detected` para campos explicitamente rotulados, com linhas de origem; duração numérica é extraída separadamente. Isso descreve a superfície do documento, não o atendimento do requisito. O observador não usa aliases, negação ou palavras do tópico para produzir uma classificação semântica. Um campo “Materiais: não usar quadro” é detectável; sua compatibilidade com a tarefa pertence a outra medida.

**Estimativa semântica da LLM:** cada um dos sete requisitos recebe obrigatoriamente um estado nominal, justificativa e lista de evidências conforme as regras abaixo. Uma ausência de rótulo não implica `not_addressed`: conteúdo pode estar em outra seção ou em paráfrase.

As sete renderizações antes problemáticas permanecem no diagnóstico lexical v2; não foram alteradas tarefas ou listas de aliases para melhorar resultados. O observador novo identifica 84/84 campos nas 12 renderizações literais nos formatos testados. É um teste de software com entrada conhecida, não acurácia semântica ou resultado de geração. Os números não são diretamente comparáveis: os instrumentos medem coisas diferentes.

## Estados semânticos

| Estado | Definição operacional autoral | Regra de evidência |
|---|---|---|
| supported | Todos os componentes explícitos do requisito estão representados compativelmente no plano. | Pelo menos uma citação do candidato. |
| partial | Há representação relevante, mas falta pelo menos um componente explícito. A justificativa deve identificar a parte não representada. | Pelo menos uma citação do candidato. |
| not_addressed | A julgadora não identifica conteúdo que trate do requisito após inspecionar o texto todo. | Lista vazia e justificativa da ausência; ausência não pode ser comprovada só pelo validador. |
| contradicted | Há declaração incompatível com componente explícito do requisito. | Pelo menos uma citação da incompatibilidade. |
| uncertain | A julgadora não consegue decidir com segurança a partir do texto. | Citação opcional e justificativa da incerteza. |

Os estados não viram valores 0/0,5/1, não têm pesos e não são somados. Não há nota global de fidelidade. Em particular, materiais, nível e duração não podem ser ignorados porque os demais campos foram considerados “centrais”.

## JSON exato e prompt

- Esquema: `experiments/judge_response.v2.schema.json`.
- Modelos tipados, prompt e parser: `src/experiment/judge_contract_v2.py`.
- `schema_version`: `eduadocs-requirement-judge-response-v2.0.0`.
- `rubric_version`: `eduadocs-requirement-judge-v2.0.0`.
- `template_version`: `lesson-plan-requirement-judge-v2.0.0`.

A raiz exige exatamente `schema_version`, `rubric_version`, `evaluation_id`, `requirements` e `assessments`. `requirements` exige exatamente topic, grade_level, learning_objectives, duration_minutes, methodology, materials e assessment_strategy. Cada resultado exige status, evidence e justification. Propriedades extras são proibidas em todos os objetos.

Cada evidência é `{line_start, line_end, quote}`. As linhas são contadas a partir de 1, com intervalo inclusivo. `quote` deve reproduzir integralmente as linhas indicadas, unidas por LF, sem números de linha adicionados, reticências, tradução ou normalização. O prompt fornece o candidato como uma lista de linhas numeradas. O parser confere os intervalos e a igualdade literal contra o texto original, não contra o alvo.

São permitidas até três evidências por item, citações de até 2.000 caracteres e justificativas de até 800 caracteres: limites técnicos de tamanho, não limiares de qualidade. Essa seleção não demonstra exaustividade das evidências ou correção da classificação. As regras condicionais entre estado e evidência são verificadas localmente, além do esquema estrito.

O parser não repara JSON. Rejeita chaves repetidas, NaN/Infinity, raiz não objeto, campos faltantes/extras, versões erradas, tipo coercível, ID divergente, justificativa em branco, ausência de evidência obrigatória e citação inventada/fora dos limites. **Uma citação autêntica ainda pode ser irrelevante ou interpretada incorretamente**; o validador não afirma ter verificado o raciocínio da LLM.

## Critérios secundários

Somente dois critérios ordinais separados são mantidos: `instructional_alignment` e `textual_coherence`, com âncoras autorais 1–4 incluídas no prompt versionado. Cada critério exige justificativa; notas 2–4 exigem evidência, nota 1 pode ter lista vazia se os componentes estiverem ausentes.

Não se produz `semantic_fidelity` global, `grade_appropriateness` ou `coherence_feasibility` na v2. Compatibilidade declarada com o nível é um dos sete requisitos; dificuldade cognitiva adequada e viabilidade real não são inferidas. A v2 não pode ser comparada numericamente aos quatro critérios v1 como se fosse a mesma escala.

## Agregação

- Por requisito e resposta: preservar os três estados e suas frequências; informar concordância exata somente com três julgamentos válidos. Havendo discordância, mostrá-la, sem atribuir um estado por maioria, calcular mediana ou converter categorias em score.
- Por tarefa/condição: resumir distribuições mantendo os denominadores de respostas e de julgamentos explícitos. Repetições não são amostras independentes.
- Para os dois critérios ordinais: mediana apenas de trincas válidas por resposta, depois síntese por tarefa/condição; trincas incompletas ficam sinalizadas. Sem nota composta ou falha técnica transformada em zero.
- No observador: três estados sintáticos por campo sobre os textos analisáveis; falhas e textos ausentes separados. `not_detected` não se transforma em `not_addressed`.
- C0 continua avaliada contra o mesmo alvo, mas só recebeu tópico e tipo de material. Essa diferença deve acompanhar a interpretação, sem informar a condição à julgadora.

## Configuração, preservação e preparação offline

A fonte única da proposta principal é `experiments/main_config.json`: Sol, reasoning low, temperatura/top_p omitidos, JSON estrito, máximo total de 4096 tokens. Os hashes do esquema, módulo do contrato e observador estão no campo `judge.contract.artifact_sha256`. A preparação recusa artefatos alterados. Uma alteração requer revisão explícita/versionada; não se deve atualizar hashes para contornar uma divergência depois de coletar dados.

Os arquivos metodológicos v1 e seus resultados permanecem intactos. A configuração principal continua em rascunho, pois fechar um contrato local não valida seu comportamento remoto nem inicia a coleta.

```powershell
.\.venv\Scripts\python.exe scripts/prepare_main_study.py
.\.venv\Scripts\python.exe scripts/observe_saved_requirements.py artifacts/pilot-qwen3-local
.\.venv\Scripts\python.exe scripts/prepare_requirement_judgments.py artifacts/pilot-qwen3-local --output artifacts/judge-contract-v2-preparation
```

O último comando apenas prepara 81 novos prompts v2 a partir das 27 respostas salvas, com IDs diferentes e vínculo separado. Nenhum foi enviado. A fila registra a origem e a configuração da nova análise; não muda a configuração usada na geração original. Não executar essa fila nos executores v1.

## Fundamentação e limites

- [FollowBench, ACL 2024](https://aclanthology.org/2024.acl-long.257/): sustenta examinar restrições individualmente; não valida nossos cinco estados nem nossos sete requisitos. O trabalho original tem verificação humana, não transferida ao nosso estudo.
- [G-Eval, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.153/): sustenta avaliação por critérios explícitos/estrutura; esta v2 não reproduz integralmente seu método nem sua validação.
- [Biggs, 1996](https://doi.org/10.1007/BF00138871): fundamenta a relação conceitual objetivos–atividades–avaliação, não a nota automática.
- [JudgeBench, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9e720fce64f91114c49cfd640d821da3-Abstract-Conference.html): motiva checar a própria julgadora com referências verificáveis; igualdade de citações é uma verificação mais estreita, não correção semântica.
- A forma técnica segue a [documentação oficial de Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs); conformidade JSON não implica acerto.

## Próxima etapa delimitada

Integrar o executor ao novo contrato e realizar uma verificação técnica limitada, seguida dos casos reservados predefinidos. Não refazer automaticamente o piloto inteiro, trocar novamente de modelo ou ajustar a rubrica até aparecer diferença favorável a C2. O consumo, truncamentos e recusas do contrato maior ainda precisam ser verificados. Nenhuma validação local substitui essa verificação ou prova confiabilidade geral.

## Verificação local desta entrega

- Suíte completa no ambiente Windows: 189 testes aprovados, incluindo parser, citações, invariância sintática, proveniência e preparação reproduzível da fila.
- 84/84 campos identificados nas renderizações literais conhecidas: verificação sintática, sem interpretação semântica.
- 81 prompts preparados; zero julgamentos executados e zero chamadas às APIs nesta etapa.
- SHA-256 dos logs originais confirmado sem alterações: gerações `8742de0ce3846f0b59af70e9227fa43f4c14a43ea5cf77df0361478752321e45`; julgamentos `802d270c8bca3a9426459fbe450321c305dc5751b031a67ddb4ca4825bbc4ddd`.

## Executor integrado

`scripts/run_requirement_judgments.py` reconstrói e confere a fila antes de chamar a API, preserva início/resultado em JSONL com bloqueio e fsync, recusa chamadas iniciadas sem resultado e não repete resultados concluídos. Interrompe o lote na primeira falha, sem tentativas automáticas. Respostas brutas e erros classificados ficam em `judgments.v2.jsonl`; frequências nominais e medianas somente de trincas válidas ficam em `summary.v2.json`. A comparação de artefatos JSON é independente das quebras de linha Windows/Linux, mantendo conferência do conteúdo integral.

Verificação sem consumo:

```powershell
.\.venv\Scripts\python.exe scripts/run_requirement_judgments.py artifacts/pilot-qwen3-local artifacts/judge-contract-v2-preparation
```

Execução limitada com créditos (padrão de uma chamada por invocação):

```powershell
.\.venv\Scripts\python.exe scripts/run_requirement_judgments.py artifacts/pilot-qwen3-local artifacts/judge-contract-v2-preparation --live --max-jobs 1
```

A integração não remove o bloqueio da coleta principal, nem substitui os testes reservados de comportamento da julgadora. A análise v2 dos planos do piloto é separada da coleta principal.

Verificação real desta integração: uma tentativa, HTTP 401 (`invalid_api_key`), zero julgamentos válidos. O lote foi interrompido na primeira falha; não houve repetição automática. Corrigir a credencial antes de novas chamadas. O erro permanece auditável no log v2 e não altera as notas do piloto v1.

### Correção da origem da credencial

O diagnóstico no Windows identificou `OPENAI_API_KEY` global de máquina diferente da chave única do `.env`; a leitura anterior priorizava a variável global. `scripts/check_openai_judge.py::read_key`, compartilhado pelos executores experimentais, agora prioriza a entrada não vazia do `.env` do projeto, com fallback para a variável do processo. Nenhuma variável global foi alterada. Teste com credenciais fictícias cobre precedência, fallback e preservação do ambiente.

Diagnóstico seguro: `.\.venv\Scripts\python.exe scripts/diagnose_openai_credential.py --check-access`. Exibe somente presença, comparação e status HTTP. A consulta de acesso não gera planos nem julgamentos.

Após a correção, a consulta de autenticação com a chave do projeto retornou HTTP 200. A recusa 401 anterior estava associada à credencial global que prevalecia sobre o `.env`.

Após corrigir a precedência, uma nova chamada real retornou HTTP 200 e julgamento v2 válido: sete requisitos e dois critérios secundários passaram pelo parser, incluindo a conferência das citações. Os dois erros 401 anteriores permanecem no log. Isso confirma compatibilidade técnica de uma resposta, não validade semântica geral. Suíte completa após a correção: 193 testes aprovados no Windows.

## Atualização operacional em 25/10/2026

A rodada diagnóstica e a execução sobre planos salvos estão documentadas em [Fechamento do piloto v2](PILOT_V2_EXECUTION_2026-10-25.md). A política original de parada foi mantida por padrão; a continuação explícita após erros de validação preserva as falhas e não reenvia respostas. Novas ondas param em falhas de API/transporte. O contrato, os prompts e os três artefatos selados não foram alterados.

## Integração ao protocolo principal congelado

Em 25/10/2026, o contrato v2 foi incorporado sem alteração de seus três artefatos selados ao [protocolo principal eduadocs-main-v1.0.0](MAIN_STUDY_PROTOCOL.md). A configuração e as fontes definidoras têm verificação de integridade antes de chamadas reais. A execução principal ainda não foi iniciada neste congelamento; o piloto mantém seu snapshot e logs próprios.
