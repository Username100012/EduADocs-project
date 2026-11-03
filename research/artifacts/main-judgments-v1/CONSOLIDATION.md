# Consolidação dos julgamentos principais — 27/10/2026

Consolidação exclusivamente local: nenhuma chamada nova às APIs. Dos 645 julgamentos, 624 são válidos, 15 falharam por divergência de citação e seis falharam por crédito. As falhas são dados ausentes, sem nota zero ou repetição.

## Notas secundárias (escala ordinal de 1 a 4)

Mediana de três julgamentos válidos por plano; depois mediana dos planos por tarefa; por fim mediana das 12 tarefas. Apenas planos com trinca válida entram nas notas. Todas as 12 tarefas estão representadas em cada célula.

| Modelo | Condição | Alinhamento instrucional | Coerência textual | Planos com trinca válida / elegíveis |
|---|---|---:|---:|---:|
| gemini | C0 | 3 | 4 | 31/36 |
| gemini | C1 | 4 | 4 | 32/35 |
| gemini | C2 | 4 | 4 | 33/36 |
| qwen3 | C0 | 3 | 3 | 33/36 |
| qwen3 | C1 | 4 | 3 | 33/36 |
| qwen3 | C2 | 4 | 3 | 34/36 |

196 dos 215 planos têm três julgamentos válidos; 19 têm trincas incompletas e não entram nas notas secundárias. Os julgamentos válidos desses planos continuam nas frequências nominais dos requisitos.

## Interpretação

C1 e C2 têm as mesmas medianas agregadas nos dois critérios e nos dois modelos. Esse empate não demonstra equivalência, ausência de diferenças por tarefa ou superioridade de C2. A escala curta apresenta concentração no limite superior, especialmente no Gemini.

C0 tem menor mediana de alinhamento instrucional nos dois modelos. Como C0 recebeu somente o tópico e o tipo de material, enquanto C1/C2 receberam os sete requisitos, essa comparação não isola o efeito da estrutura do prompt. A comparação C1/C2 mantém a informação e altera sua organização.

Os sete requisitos são categorias nominais (supported, partial, not_addressed, contradicted, uncertain), apresentadas separadamente em RESULTS.md e nos CSVs. Não foram convertidas em pontuação numérica, nota global ou decisão por maioria. O denominador de cada célula é seu número de julgamentos válidos, não 108 automaticamente.

As repetições não são participantes independentes. Notas da julgadora são estimativas automatizadas, não validação pedagógica, verificação factual ou evidência de eficácia em sala de aula. Não foram realizados testes de significância.

## Conferência

As 624 respostas válidas foram reprocessadas pelo parser e produziram exatamente os registros validados salvos. As 15 falhas de citação foram reproduzidas. Denominadores e agregação das notas foram recalculados independentemente; resultado em consolidation_audit.json. Dados brutos não alterados.

Arquivos: RESULTS.md (frequências e notas), results_tables.json (dados por tarefa), requirements_by_condition.csv, requirements_by_task.csv e secondary_scores_by_condition.csv.

Análise dos sete requisitos concluída: [comparação C0/C1/C2 e detalhamento C1/C2 por tarefa](REQUIREMENTS_COMPARISON.md), com distribuições nominais completas e denominadores verificados. [CSV C1/C2 por tarefa](c1_c2_requirements_by_task.csv). Sem chamadas novas às APIs ou mudanças no protocolo.

Auditoria computacional exploratória concluída: [casos, evidências e limitações](case-audit/AUDIT.md). Identificados defeitos dos planos, um erro aritmético verificável da julgadora e variação na interpretação de objetivos. Classificações principais preservadas; zero chamadas adicionais às APIs.
