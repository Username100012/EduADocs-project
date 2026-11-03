# Indicadores automáticos da coleta principal — 26/10/2026

Análise local concluída das 216 tentativas e 215 textos, mantendo o timeout Gemini C1 como falha sem texto, sem zero artificial e sem repetição. Não houve novas chamadas às APIs ou julgamentos GPT.

## Instrumentos e integridade

Foram executados o observador `eduadocs-requirement-observations-v1` e a extração numérica temporal congelada. A nova rotina `scripts/summarize_main_observations.py` implementa a consolidação descritiva já prevista: 78 estratos, seis globais gerador/condição e 72 por tarefa/gerador/condição. Não modifica detectores, aliases, payloads, prompts ou limiares após observar os resultados. Seu hash e o do agregador de quartis estão no JSON de saída.

Os 215 textos têm observações por sete campos; os denominadores são 36 por célula, exceto Gemini C1, com 35 textos e um timeout. Tabelas de latência e tokens apresentam medianas por tarefa, seguidas da mediana entre tarefas com pesos iguais; o JSON/CSV também preserva as distribuições entre respostas. Frequências de campos são contagens sobre os textos disponíveis, com recortes por tarefa e área no CSV, não scores agregados de atendimento.

O log original conserva SHA-256 `70969e6fe4df45f92d7dd9605eb68cb90b6dfa9eaa6d0346bb2f1f1a4b5b4135`. O protocolo e as fontes seladas permaneceram intactos. As tabelas foram recalculadas e reproduzidas byte a byte. Suíte Windows: 212 testes aprovados, incluindo denominadores, ausências, duplicação de textos e custo com raciocínio contado uma única vez.

## Achados computacionais restritos

| Gerador | Condição | Textos | Declaração de duração igual ao alvo | Diferente | Indeterminada | Textos distintos |
|---|---|---:|---:|---:|---:|---:|
| Gemini | C0 | 36 | 3 | 27 | 6 | 36 |
| Gemini | C1 | 35 | 35 | 0 | 0 | 35 |
| Gemini | C2 | 36 | 36 | 0 | 0 | 36 |
| Qwen3 | C0 | 36 | 0 | 29 | 7 | 29 |
| Qwen3 | C1 | 36 | 34 | 2 | 0 | 29 |
| Qwen3 | C2 | 36 | 36 | 0 | 0 | 24 |

O alvo é 50 minutos. Correspondência da declaração não comprova soma correta das etapas ou viabilidade de aula. O extrator congelado não soma títulos arbitrários de etapas. C0 não recebeu o alvo de duração e outros cinco requisitos; sua divergência não comprova inferioridade de modelo nem efeito isolado da estrutura.

Nos indicadores operacionais, as medianas entre tarefas de latência foram 18,08/15,96/14,89 s para Gemini C0/C1/C2 e 23,02/28,19/23,38 s para Qwen3. Não são efeitos causais isolados de modelo ou estrutura: carga, rede, hardware, tamanho e configuração variam. Textos repetidos e três gerações de uma tarefa não são tarefas independentes.

## Limite observado do instrumento de campos

Foram preservados 79 estados `empty`, com rótulo reconhecido e contexto original em `automatic_measurement_audit.v1.json`. Esse é um estado do parser: não demonstra seção realmente vazia. Há casos com conteúdo imediatamente após o rótulo, mas que as regras não associaram ao campo. Por exemplo, uma seção de avaliação seguida de itens “Formativa” e “Entrega”, ou materiais descritos como lista numerada de subtítulos, pode receber esse estado. Também podem existir tópicos em títulos ou nível descrito em uma frase sem rótulo reconhecido.

Não foram recodificados esses casos nem ajustadas regras com os resultados principais. As frequências devem ser apresentadas como detectabilidade pelos padrões congelados, nunca taxa de omissão ou cumprimento semântico. Esse limite será separado da estimativa da julgadora, que também não constitui verdade de referência ou validação pedagógica.

## Consumo e custo

As 107 respostas Gemini com consumo reportado têm estimativa bruta conjunta de US$ 0,554391, sem desconto de cache e usando os preços de referência congelados. A saída total é inferida de total_tokens menos input_tokens, incluindo raciocínio; o custo do timeout permanece desconhecido. Não é fatura ou estimativa completa da conta, e energia local não foi medida. Nenhum custo OpenAI novo foi gerado nesta etapa.

## Artefatos e próximo passo

- [Relatório legível](../artifacts/main-study-v1/AUTOMATIC_METRICS.md).
- `artifacts/main-study-v1/automatic_summary.v1.json`: indicadores, cobertura, hashes e agregações.
- `automatic_fields.v1.csv`: campos por tarefa, área, condição e gerador.
- `automatic_operations.v1.csv`: latência, tokens e tamanho textual, com agregação identificada.
- `automatic_duration.v1.csv`: resultados de duração, mantendo indeterminados.
- `requirement_observations.v1.json`: evidências por linha e observações dos textos.
- `automatic_measurement_audit.v1.json`: contextos dos 79 estados empty, sem relabeling.

Próximo passo: preparar e conferir a fila de 645 julgamentos (três por plano elegível), antes de executá-la sob o contrato v2. Nenhum julgamento foi realizado por esta análise. Não se conclui superioridade semântica de C2 a partir destes indicadores.
