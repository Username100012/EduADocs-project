# Texto-base para o artigo: avaliação computacional do piloto

Versão para revisão dos autores, baseada exclusivamente nos dados salvos do piloto. O estudo principal de 12 tarefas e dois geradores não foi executado nesta etapa. Os números abaixo não devem ser apresentados como resultados desse estudo principal.

## Método

A avaliação computacional foi conduzida sobre tarefas sintéticas de geração de planos de aula em três áreas introdutórias da Computação: Algoritmos, com busca linear em vetores; Banco de Dados, com consultas SQL utilizando SELECT e WHERE; e Engenharia de Software, com requisitos funcionais e não funcionais de um sistema de biblioteca. O mapeamento curricular utiliza o referencial da Sociedade Brasileira de Computação como orientação ampla, enquanto a seleção dos tópicos e a elaboração das tarefas constituem operacionalizações dos autores, sem validação curricular externa.

Foram comparadas três condições de entrada: C0, contendo apenas tipo de material e tópico; C1, com os sete requisitos apresentados em texto livre; e C2, com instrução estruturada derivada da mesma instância de dados de C1. Os requisitos foram tópico, nível de ensino, objetivos de aprendizagem, duração, metodologia, materiais e estratégia de avaliação. Dessa forma, C0/C1 introduz informação adicional, enquanto C1/C2 permite examinar a organização da instrução mantendo seu conteúdo informacional. Esse desenho não constitui ablação individual dos sete requisitos.

O gerador local Qwen3 4B, com quantização Q4_K_M, foi executado via Ollama, produzindo três respostas por tarefa e condição, totalizando 27 planos. Os parâmetros e as respostas originais permanecem registrados nos logs. A utilização de seed fixa e a ocorrência de textos idênticos impedem interpretar as repetições como observações independentes. Foram identificados seis textos distintos em C0, sete em C1 e cinco em C2, entre nove gerações por condição.

A mensuração foi dividida em observações sintáticas locais e estimativas semânticas de uma LLM julgadora. O observador identifica campos rotulados detectados, vazios ou não detectados e extrai declarações temporais reconhecíveis; essas observações não equivalem a cumprimento semântico. A decomposição por requisito é informada por FollowBench ([Jiang et al., 2024](https://aclanthology.org/2024.acl-long.257/)), sem reproduzir integralmente seu protocolo ou transferir sua validação humana ao presente estudo.

A julgadora GPT `gpt-6.1-sol`, com esforço de raciocínio baixo, temperatura e top_p omitidos e limite de 4096 tokens, recebeu o alvo completo e o plano sob identificador opaco, sem indicação explícita da condição ou do gerador. Essa omissão de metadados não garante cegamento absoluto, pois características do conteúdo podem revelar a condição. Para cada requisito, a julgadora atribuiu um estado nominal: atendimento sustentado pelo texto, parcial, não abordado, contradito ou incerto. Cada decisão incluiu justificativa; atendimento, atendimento parcial e contradição exigiram citações literais do plano. O parser verificou esquema, tipos, identificador, intervalos de linhas e correspondência literal das citações. Uma citação autêntica não comprova a pertinência da evidência ou o acerto da interpretação.

Dois critérios secundários foram estimados em escala ordinal autoral de 1 a 4: relação textual entre objetivos, atividades e avaliação; e coerência textual. A avaliação por critérios explícitos é informada por G-Eval ([Liu et al., 2023](https://aclanthology.org/2023.emnlp-main.153/)); o conceito de alinhamento apoia-se em [Biggs (1996)](https://doi.org/10.1007/BF00138871). Essas referências não validam a escala proposta nem demonstram sua adequação automática a planos de aula em português.

Antes da execução do restante do lote, realizou-se uma rodada diagnóstica separada sobre um plano sintético novo de fila FIFO, em seis versões: base, alteração de formatação, aumento de verbosidade, omissão de materiais, avaliação desalinhada e cronograma contraditório. As expectativas foram registradas antes das chamadas, com três julgamentos por versão, totalizando 18 respostas. Os casos foram inspecionados no desenvolvimento do software; não constituem benchmark externo ou conjunto cegado por terceiros. A checagem da própria julgadora é motivada por trabalhos como [JudgeBench, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9e720fce64f91114c49cfd640d821da3-Abstract-Conference.html), sem reproduzir esse benchmark.

Cada plano do piloto teve três julgamentos planejados. Os cinco estados por requisito foram mantidos como categorias nominais, sem pontuação, mediana ou veredito por maioria. Para os dois critérios ordinais, calculou-se a mediana somente de trincas válidas por plano, seguida da mediana por tarefa e da mediana entre tarefas. Falhas não receberam nota zero. A análise é descritiva, sem testes de significância ou score composto.

## Resultados

As 18 respostas da rodada diagnóstica passaram pelo contrato local e as seis verificações predefinidas foram satisfeitas. No conjunto testado, a julgadora manteve as classificações sob alterações de formatação e verbosidade e identificou os defeitos explícitos introduzidos. O resultado caracteriza o comportamento observado em um tópico e não uma estimativa de acurácia geral.

No piloto, as 81 avaliações planejadas resultaram em 80 julgamentos válidos. Houve 83 tentativas operacionais: dois erros históricos HTTP 401 foram recuperados uma única vez, após a correção da credencial, em log separado e com as mesmas requisições. Uma resposta produzida pelo modelo permaneceu inválida por divergência literal entre citação e origem: foram omitidos espaços finais. Não houve reparo da resposta ou nova tentativa desse julgamento. Assim, C0 e C2 apresentaram nove planos com trincas válidas, enquanto C1 apresentou oito trincas completas e um plano com dois julgamentos válidos.

| Condição | Julgamentos válidos | Planos com trincas válidas | Alinhamento textual¹ | Coerência textual¹ |
|---|---:|---:|---:|---:|
| C0 | 27/27 | 9/9 | 3 | 4 |
| C1 | 26/27 | 8/9 | 4 | 4 |
| C2 | 27/27 | 9/9 | 4 | 3 |

¹ Mediana entre tarefas, após agregação das trincas válidas por plano e das respostas por tarefa. Escalas autorais secundárias, sem validação pedagógica.

Na classificação nominal, o tópico recebeu atendimento sustentado em todos os julgamentos válidos. Em C0, a duração foi classificada como contradita em 27 de 27 julgamentos, enquanto materiais e estratégia de avaliação foram classificados como parciais em 27 de 27. Como C0 não recebeu seis requisitos do alvo, esses resultados descrevem a diferença de informação disponível e não demonstram inferioridade do modelo.

Em C1, seis requisitos receberam atendimento sustentado nos 26 julgamentos válidos. Para duração, foram observados 23 julgamentos de atendimento e três de contradição, estes referentes ao mesmo plano. Uma checagem computacional específica das seis etapas numeradas desse plano confirmou a soma de 5 + 10 + 25 + 10 + 10 + 5 = 65 minutos, em contraste com os 50 minutos declarados. O extrator temporal geral reconhecia a declaração de 50 minutos, mas não somava essas etapas: trata-se de uma diferença documentada entre instrumentos, e não de validação geral da julgadora.

Em C2, cada um dos sete requisitos recebeu atendimento sustentado nos 27 julgamentos válidos. Esse resultado pertence à estimativa da julgadora e não significa verificação factual ou pedagógica independente. A presença de classificações concentradas na categoria superior também limita a capacidade de discriminar diferenças entre C1 e C2.

As categorias nominais apresentaram concordância exata nas sete dimensões em todas as 26 trincas completas. Nos critérios ordinais, a concordância não foi total: em alinhamento textual, ocorreu em 7/9, 8/8 e 8/9 trincas para C0, C1 e C2; em coerência textual, em 9/9, 6/8 e 7/9. Estabilidade de categorias e citações válidas não equivalem a validade semântica.

As medianas de latência de geração previamente registradas foram 22,45 s em C0, 28,11 s em C1 e 23,47 s em C2, com IQR de 0,65 s, 3,66 s e 1,06 s, respectivamente. São medidas do ambiente e das tarefas do piloto, sujeitas a carregamento, execução e dependência entre repetições; não demonstram vantagem causal geral. As latências de julgamento foram registradas separadamente, com concorrência limitada, e não são intercambiáveis com os tempos de geração.

## Discussão e limites

O piloto oferece evidência descritiva de que explicitar os requisitos em C1 e C2 se associa a maior atendimento estimado do alvo do que omiti-los em C0. Entretanto, a comparação que controla a informação, C1/C2, não sustenta superioridade global da instrução estruturada: ambas atingiram a mesma mediana de alinhamento, enquanto C2 apresentou mediana inferior de coerência textual. A melhora observada na classificação temporal de C2 refere-se a um conjunto pequeno e dependente, sem inferência estatística.

O estudo foi restrito a três tarefas, um gerador local, uma configuração de julgadora e planos de aula. Não avalia os demais módulos do EduADocs, o desempenho de geradores comerciais, correção factual/algorítmica sistemática, aprendizagem de estudantes ou qualidade pedagógica global. O identificador da julgadora não é snapshot datado, e a execução ocorreu em momentos diferentes, exigindo cautela quanto à reprodução futura. A falha de correspondência literal mostra que o contrato pode rejeitar uma resposta por diferença de espaços mesmo quando não há evidência fabricada; essa rejeição foi preservada como limitação técnica.

Não houve participação de docentes ou estudantes como avaliadores. Portanto, não se fazem afirmações de concordância humana, usabilidade SUS, eficácia educacional ou validação por especialistas. A disponibilização de prompts, esquema, logs e tabelas permite auditoria do processamento, mas não substitui verificadores independentes dos construtos semânticos. A ampliação para novas tarefas e geradores é uma etapa distinta, ainda não executada.

## Fontes locais para conferência

- Tabelas completas: `artifacts/judge-contract-v2-preparation/RESULTS.md` e `results_tables.json`.
- Frequências: `requirements_by_condition.csv` e `requirements_by_task.csv`, no mesmo diretório.
- Revalidação das 80 respostas brutas e verificação temporal específica: `evidence_audit.json`.
- Diagnóstico: `artifacts/reserved-requirement-v2/relations_report.json`.
- Logs originais de geração e julgamento v1 preservados; recuperação de autenticação em `artifacts/judge-auth-recovery-v2/`.
- Histórico das decisões operacionais: [fechamento do piloto v2](PILOT_V2_EXECUTION_2026-10-25.md).
