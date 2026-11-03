# Fontes para a metodologia — estudo principal

Conferência em 02/11/2026. Os artefatos abaixo estão no workspace local `C:\Users\Jeffe\eduadocs`. A main pública do GitHub contém a aplicação e parte de `src/experiment`, mas não contém `experiments/`, `scripts/` ou `artifacts/`. Nas duas pastas Eduadocs acessíveis pelo Google Drive foram encontrados documentos de planejamento, qualificação e TCC; não foi localizada cópia dos logs principais.

## Ler nesta ordem

1. [Protocolo principal congelado](MAIN_STUDY_PROTOCOL.md).
2. [Configuração exata](../experiments/main_config.json) e [selo SHA-256](../experiments/main_config.json.sha256): 12 tarefas e seus sete requisitos, condições, parâmetros, execução, julgadora e plano de análise.
3. [Log de geração](../artifacts/main-study-v1/generations.jsonl): cabeçalho com configuração e plano, eventos de início e resultado, prompts, respostas, erros, latência e consumo quando reportado. [Resumo da coleta](../artifacts/main-study-v1/collection_summary.json).
4. [Contrato efetivamente usado pela julgadora v2](REQUIREMENT_JUDGE_CONTRACT_V2.md), [esquema JSON](../experiments/judge_response.v2.schema.json) e [implementação do prompt/parser](../src/experiment/judge_contract_v2.py).
5. [Requisições de julgamento preparadas](../artifacts/main-judgments-v1/queue.jsonl), [mapeamento para tarefas/condições](../artifacts/main-judgments-v1/mapping.jsonl) e [julgamentos brutos](../artifacts/main-judgments-v1/judgments.v2.jsonl). [Estado final](../artifacts/main-judgments-v1/execution_status.json).
6. [Indicadores automáticos](../artifacts/main-study-v1/AUTOMATIC_METRICS.md), [tabelas dos julgamentos](../artifacts/main-judgments-v1/RESULTS.md), [dados consolidados](../artifacts/main-judgments-v1/results_tables.json).
7. Análises posteriores separadas: [auditoria exploratória dos casos](../artifacts/main-judgments-v1/case-audit/AUDIT.md) e [sensibilidade por pares completos](../artifacts/main-judgments-v1/paired-complete-sensitivity/RESULTS.md).

## Procedimentos aplicados e composição

- Geração: 12 tarefas × 3 condições × 2 geradores × 3 repetições = 216 tentativas. Foram obtidos 215 textos e um ReadTimeout Gemini C1, tarefa 002, repetição 1. As retomadas enviaram somente IDs não tentados; o ID com falha não foi repetido.
- Modelos geradores: gemini-3.8-flash e qwen3:4b-q4_K_M. O GPT gpt-6.1-sol foi julgador, não terceiro gerador. Parâmetros completos estão na configuração e no cabeçalho do log.
- Julgamentos principais: 215 planos × 3 = 645 tentativas, com 624 válidas, 15 falhas de citação e seis erros de crédito. A retomada preservou os erros e processou somente IDs não enviados.
- Foram aplicados observador sintático/temporal congelado e contrato semântico v2, com cinco categorias nominais por requisito e dois critérios ordinais secundários. As notas usam 196 trincas completas; as frequências nominais usam todos os julgamentos válidos. Não houve avaliação humana, SUS, teste de significância ou score composto.
- Auditoria de casos e sensibilidade com pares completos foram análises exploratórias posteriores, não partes originalmente pré-especificadas do protocolo principal.

## Scripts para conferir o processamento

- [Executor de geração](../scripts/run_pilot.py) e [implementação compartilhada](../src/experiment/pilot_runner.py). O nome do script inclui pilot, mas a coleta principal usa main_config.json e diretório separado.
- [Observações locais](../scripts/observe_saved_requirements.py) e [agregação operacional](../scripts/summarize_main_observations.py).
- [Preparação dos julgamentos](../scripts/prepare_requirement_judgments.py), [executor](../scripts/run_requirement_judgments.py) e [tabelas](../scripts/report_requirement_results.py).
- [Auditoria exploratória](../scripts/audit_saved_qwen_cases.py) e [sensibilidade pós-coleta](../scripts/analyze_paired_complete_cases.py).

## Distinções necessárias

Os documentos e manifestos v1 e os diretórios de piloto/diagnóstico são históricos; não devem ser descritos como se fossem a avaliação principal v2. O arquivo data/executions.jsonl da aplicação registra gerações operacionais e não substitui generations.jsonl e judgments.v2.jsonl do experimento. A versão atual de produção recebeu correções posteriores de seleção de modelo, DOCX e download de registro; essas correções não foram retroaplicadas aos dados científicos.

A conferência de localização não publicou novos arquivos no GitHub ou Drive. Nenhuma API de geração ou julgamento foi chamada.
