# Auditoria das métricas do piloto local

27 respostas; 189 células de requisitos. As métricas v1 foram reproduzidas a partir do log original. Respostas, configuração e métricas originais foram preservadas.

Correspondência é evidência lexical; não é conformidade semântica. Não correspondência não comprova omissão. Indeterminado significa que o extrator não decidiu.

## Por condição (9 respostas em cada condição)

| Requisito | Condição | Correspondência | Não correspondência | Indeterminado | Correspondência no texto fora do escopo reconhecido |
|---|---|---:|---:|---:|---:|
| Tópico | C0 | 9 | 0 | 0 | 0 |
| Tópico | C1 | 9 | 0 | 0 | 0 |
| Tópico | C2 | 9 | 0 | 0 | 0 |
| Nível escolar | C0 | 9 | 0 | 0 | 0 |
| Nível escolar | C1 | 9 | 0 | 0 | 0 |
| Nível escolar | C2 | 9 | 0 | 0 | 0 |
| Objetivos | C0 | 4 | 1 | 4 | 2 |
| Objetivos | C1 | 7 | 0 | 2 | 2 |
| Objetivos | C2 | 2 | 0 | 7 | 7 |
| Duração | C0 | 0 | 6 | 3 | 0 |
| Duração | C1 | 8 | 0 | 1 | 0 |
| Duração | C2 | 7 | 0 | 2 | 0 |
| Metodologia | C0 | 0 | 0 | 9 | 0 |
| Metodologia | C1 | 4 | 0 | 5 | 3 |
| Metodologia | C2 | 0 | 0 | 9 | 4 |
| Materiais | C0 | 0 | 1 | 8 | 0 |
| Materiais | C1 | 1 | 0 | 8 | 8 |
| Materiais | C2 | 0 | 0 | 9 | 9 |
| Avaliação | C0 | 0 | 8 | 1 | 0 |
| Avaliação | C1 | 0 | 1 | 8 | 7 |
| Avaliação | C2 | 0 | 0 | 9 | 9 |

## Diagnóstico e consequências

- O reconhecimento de seções exige rótulos específicos com dois-pontos e não trata uniformemente títulos numerados e campos em listas. A busca no texto inteiro, com os mesmos aliases, revela evidências perdidas pelo escopo; ela pode incluir exemplos e menções incidentais e não substitui a métrica.
- O nível escolar conta qualquer menção de graduação/ensino superior, inclusive planos que também mencionam ensino médio. Não mede adequação ao nível nem exclusividade do público-alvo.
- Objetivos verificam verbos e conceitos, sem comprovar todos os resultados esperados. Metodologia exige aliases restritos. Materiais e avaliação dependem de seções reconhecidas. Não há validação de qualidade desses requisitos.
- A heurística de negação pode confundir 'não funcionais' com contexto negado. Não se deve resolver isso adicionando aliases apenas para melhorar estes resultados.
- A duração v1 pode interpretar '2 aulas (90 minutos cada)' como 90, sem multiplicar; também ignora 'Duração da aula'. O cronograma em etapas com minutos não é somado. Ausência de contradição detectada não prova consistência.
- C0 recebe apenas tipo de material e tópico. Compará-la aos outros seis requisitos é comparação contra um alvo não informado, e não desobediência a instruções recebidas.
- A dependência da formatação pode distorcer C1 versus C2. Não usar esta tabela para afirmar superioridade de uma condição; não calcular nota composta.

## Evidências auditáveis

Cada uma das 189 células, seus trechos e linhas, flags e diagnóstico no texto inteiro está em `metrics_audit.json`; o mesmo arquivo contém os 63 agrupamentos por tarefa, condição e requisito. Os hashes vinculam a auditoria aos arquivos de origem.

- `duration_label_not_supported`: `qwen3:pilot-002:c1:r1`, requisito `duration_minutes`, linha 8: **Duração da aula:** 50 minutos  
- `schedule_not_extracted_not_proof_of_consistency`: `qwen3:pilot-002:c1:r1`, requisito `duration_minutes`.
- `lexical_evidence_outside_recognized_section`: `qwen3:pilot-002:c1:r1`, requisito `methodology`.
- `nonfunctional_term_can_trigger_negation_heuristic`: `qwen3:pilot-003:c1:r1`, requisito `topic`.
- `mixed_school_levels_mention_not_target_specificity`: `qwen3:pilot-001:c0:r2`, requisito `grade_level`.
- `multiple_lessons_not_multiplied`: `qwen3:pilot-001:c0:r2`, requisito `duration_minutes`, linha 9: - **Carga horária:** 2 aulas (45 minutos cada)  

Foram sinalizadas 3 ocorrências de caracteres CJK; são alertas técnicos de conteúdo a investigar, não uma classificação validada de idioma.

- `qwen3:pilot-001:c2:r1`, linha 49:   会被
- `qwen3:pilot-001:c2:r3`, linha 49:   会被
- `qwen3:pilot-001:c2:r2`, linha 49:   会被

## Próximo passo isolado

Construir testes de invariância à formatação com exemplos sintéticos e corrigir o extrator em uma nova versão. Congelar as regras antes da coleta principal; recalcular este piloto como análise exploratória, preservando v1. Não regenerar planos nem alegar que ajustes feitos após observar o piloto constituem validação independente.
