# Documentation

## Coleta principal concluída — 26/10/2026

As 216 tentativas foram concluídas em `artifacts/main-study-v1`: 215 planos gerados e um ReadTimeout Gemini preservado. IDs completos e únicos, sem chamadas pendentes, fontes seladas inalteradas. [Resumo final](../artifacts/main-study-v1/README.md). Piloto preservado; julgamentos GPT ainda não executados. Há 215 respostas elegíveis, correspondentes a até 645 julgamentos.

## Protocolo principal congelado — 25/10/2026

[Protocolo final](MAIN_STUDY_PROTOCOL.md) · [Revisão, verificações e selo](MAIN_STUDY_REVIEW_AND_FREEZE.md).

`eduadocs-main-v1.0.0`: 12 tarefas, 216 gerações e até 648 julgamentos. Configuração única e hashes verificados no Windows. Revisão exclusivamente local; nenhuma chamada de coleta foi iniciada. Próximo passo: execução em diretório novo, com verificação automática das versões e do modelo local.

## Estado do piloto — 25/10/2026

Piloto v2 concluído: 27 planos, 81 avaliações únicas, 80 julgamentos válidos, uma falha literal de citação preservada; 26 trincas completas. Diagnóstico separado: 18 julgamentos válidos e seis relações predefinidas satisfeitas. Não houve novas gerações de planos. O piloto permanece separado do estudo principal, agora congelado em versão local.

- [Texto-base de método, resultados e discussão para o artigo](ARTICLE_COMPUTATIONAL_PILOT_V2.md).
- [Tabelas completas do piloto](../artifacts/judge-contract-v2-preparation/RESULTS.md).
- [Decisões operacionais e limites](PILOT_V2_EXECUTION_2026-10-25.md).

This directory contains technical documentation for the EduADocs - Document Generator project.

## Available Documentation

### Fix and Implementation Notes

- **[Ollama Cleanup Fix](./OLLAMA_CLEANUP_FIX.md)** - Implementation of thinking tags cleanup for Ollama models

### Project Variants

- **[Simplified Version](../simplified/README_simple.md)** - Documentation for the simplified version of the application
- **[Streamlined Version](../streamlined/README_streamlined.md)** - Documentation for the streamlined version of the application
- **[Version Comparison](../streamlined/COMPARISON.md)** - Comparison between different project versions

## Project Structure

For the main project documentation and setup instructions, see the [main README](../README.md) in the root directory.

## Contributing

When adding new documentation:

1. Place technical fixes and implementation notes in this `docs/` directory
2. Use descriptive filenames that clearly indicate the content
3. Update this index file to include links to new documentation
4. Follow the existing markdown formatting conventions
# Avaliação computacional — estado em 19/10/2026

Para a etapa experimental, começar por estes documentos. Os arquivos de protocolo e rubricas anteriores permanecem como histórico; suas escalas e testes não são ativados automaticamente na proposta atual.

- [Matriz de dimensões, referências e métricas](COMPUTATIONAL_EVALUATION_MATRIX.md).
- [Protocolo principal proposto e pendências](MAIN_STUDY_PROTOCOL.md): 12 tarefas, 216 gerações previstas, até 648 julgamentos; rascunho sem coleta principal iniciada.
- [Preparação offline e catálogo](../artifacts/main-preparation/PREPARATION.md), com diagnóstico de sete payloads cujo texto literal expõe limites das regras lexicais.
- [Indicadores principais do piloto](../artifacts/pilot-qwen3-local/PRIMARY_METRICS_V2.md), sem score composto ou conclusão de qualidade pedagógica.
- [Comparação exploratória das julgadoras](../artifacts/judge-sensitivity-sol-v1/COMPARISON.md).

Configuração única proposta para a etapa principal: `experiments/main_config.json`. A configuração do piloto e os artefatos metodológicos congelados não foram reescritos. Última verificação completa no Windows: 212 testes aprovados; nenhuma chamada à API nesta preparação.


## Contrato de mensuração atual

[Mensuração e julgadora v2](REQUIREMENT_JUDGE_CONTRACT_V2.md): sete requisitos com cinco categorias nominais, evidências por linhas e duas notas secundárias. Esquema, prompt e parser fechados localmente; sem execução de APIs nesta etapa. Preparação offline em `artifacts/judge-contract-v2-preparation/`; integração do executor principal ainda pendente.

Executor v2 integrado em `scripts/run_requirement_judgments.py`. A tentativa real limitada recebeu HTTP 401 (`invalid_api_key`); lote interrompido, sem julgamentos válidos. Corrigir credencial antes de prosseguir.

Conflito de credencial corrigido: scripts experimentais priorizam a chave não vazia do `.env` sobre a variável global do Windows. Autenticação do projeto confirmada com HTTP 200; a variável global não foi alterada.

Verificação após correção: um julgamento real v2 recebido e validado com sucesso (sete requisitos e dois critérios); dois erros de autenticação anteriores preservados no log.

Verificação Gemini em 25/10/2026: metadados do modelo acessíveis, mas geração mínima recusada com HTTP 402 (créditos Prepay esgotados). [Diagnóstico e ação necessária](GEMINI_MAIN_PREFLIGHT_2026-10-25.md). Coleta principal permanece bloqueada; nenhuma compra ou recarga automática foi realizada.

Atualização Gemini: repetição após regularização bem-sucedida (`OK`, 8 tokens totais). O bloqueio 402 não ocorreu no novo teste. Próxima etapa: revisão e congelamento do protocolo, antes da coleta principal.

Orçamento Gemini concluído: [estimativa conservadora](../artifacts/gemini-main-budget-2026-10-25/BUDGET.md). Contados 36 prompts únicos pelo provedor; 108 gerações previstas, entrada total de 12.663 tokens e teto de saída de 442.368 tokens. Estimativa com câmbio de planejamento R$ 6/US$ e reserva de 25%: R$ 12,52. O usuário aceita ultrapassar R$ 30; não houve redução do desenho nem início de coleta. Julgamentos GPT não estão incluídos.

Indicadores automáticos principais concluídos em 26/10/2026: [análise e limites](MAIN_AUTOMATIC_ANALYSIS_2026-10-26.md) e [tabelas](../artifacts/main-study-v1/AUTOMATIC_METRICS.md). 215 textos, timeout separado, zero chamadas novas às APIs. Estados de detecção são do instrumento, não prova de cumprimento ou omissão.

Fila principal conferida offline: [645 julgamentos preparados](../artifacts/main-judgments-v1/README.md), com três repetições para cada um dos 215 planos elegíveis. Auditoria de IDs, hashes, requisições e configuração congelada concluída; nenhuma chamada GPT executada.

Julgamentos principais iniciados em 26/10/2026: [execução de 645 avaliações](../artifacts/main-judgments-v1/README.md), com a fila já conferida, seis chamadas por onda e registro append-only. Os dados de geração e o protocolo permanecem inalterados.

Julgamentos principais interrompidos após 72 tentativas por `credit_balance_exhausted`: 65 válidos, uma falha de citação e seis erros de saldo; 573 não enviados. [Estado e retomada](../artifacts/main-judgments-v1/README.md). Fila e gerações originais preservadas.

Julgamentos principais concluídos em 27/10/2026: 645 tentativas, 624 válidas, 15 falhas de validação e seis erros de crédito anteriores preservados. Zero chamadas pendentes, IDs repetidos ou alterações nos dados de geração e fila. [Estado final auditado](../artifacts/main-judgments-v1/execution_status.json). Próxima etapa: consolidação offline dos resultados sob o protocolo congelado.

Consolidação principal concluída em 27/10/2026: [notas por modelo e condição e limites de interpretação](../artifacts/main-judgments-v1/CONSOLIDATION.md). 624 respostas revalidadas, 15 erros de citação reproduzidos e 196/215 trincas completas. C1/C2 empatam nas medianas agregadas; isso não prova equivalência. Zero chamadas novas às APIs.

Análise dos sete requisitos concluída em 27/10/2026: [comparação por modelo, condição e tarefa](../artifacts/main-judgments-v1/REQUIREMENTS_COMPARISON.md). Verificados 42 estratos por requisito e condição e 504 por tarefa; C1/C2 têm resultados mistos, sem superioridade geral demonstrada. Dados e protocolo preservados; nenhuma API executada.

Auditoria local concluída em 27/10/2026: [72 planos Qwen3 C1/C2 em duração e 12 em objetivos](../artifacts/main-judgments-v1/case-audit/AUDIT.md). Inclui erro aritmético demonstrável da julgadora, inconsistências reais e limites de interpretação; análise exploratória sem recodificação dos resultados ou novas APIs.

Rascunho integrado do estudo principal em 27/10/2026: [Resultados e limitações](ARTICLE_MAIN_RESULTS_AND_LIMITATIONS.md). Reúne 215 planos, 624 julgamentos válidos, latência/tokens e auditoria exploratória, sem dados do piloto nem chamadas novas às APIs. [CSV integrado](../artifacts/main-judgments-v1/integrated_results.csv) e hashes em integration_audit.json.

Análise pós-coleta de sensibilidade concluída em 28/10/2026: [pares completos C1/C2](../artifacts/main-judgments-v1/paired-complete-sensitivity/RESULTS.md), com 30 pares Gemini e 31 Qwen3, todas as 12 tarefas preservadas. Medianas gerais e direções dos contrastes agrupados mantidas; não elimina viés de seleção. [Contribuição e conclusão propostas](MAIN_STUDY_CONTRIBUTION.md); rascunho do artigo atualizado. Zero APIs e dados principais inalterados.
