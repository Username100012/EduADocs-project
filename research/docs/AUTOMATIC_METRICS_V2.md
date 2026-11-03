# Extrator de métricas v2

Implementação: `src/experiment/automatic_metrics_v2.py`, versão `eduadocs-textual-proxies-v2`.

A v1 permanece em `automatic_metrics.py`; os scripts existentes continuam usando v1. Esta etapa não recalcula o piloto, não altera prompts, respostas, aliases das tarefas ou configuração experimental e não chama modelos. A v2 foi desenvolvida após observar falhas do piloto: os testes sintéticos verificam o comportamento do software, sem constituir validação independente das métricas.

## Mudanças

- Reconhecimento dos rótulos documentados com ou sem dois-pontos, em títulos Markdown, negrito, listas e numeração hierárquica. Campos em linha e títulos seguidos por conteúdo compartilham a mesma regra de escopo. As evidências mantêm texto e linha originais.
- Rótulos de objetivos, metodologia, materiais/recursos e avaliação continuam delimitando o escopo. Referências, conteúdo, metadados e novos títulos reconhecidos encerram a seção anterior. Não há fallback para buscar o requisito no documento inteiro.
- A expressão técnica “não funcional/não funcionais” não é tratada por si só como instrução negada; a categoria positiva “funcional/funcionais” continua excluída desse trecho. Outras negações continuam gerando incerteza por uma heurística conservadora.
- Duração aceita “Duração”, “Duração total”, “Duração da aula” e “Carga horária”, inclusive valor na próxima linha não vazia. Horas e minutos são normalizados; “2 aulas (45 minutos cada)” resulta em 90 minutos. Quantidades sem indicação “cada”, declarações não numéricas ou combinações ambíguas com “total” ficam sem extração. A numeração de título não remove o valor “90 minutos”.
- `target_mismatch_detected` separa divergência contra o alvo de `internal_inconsistency_detected`, que compara durações extraídas entre si. Sem valores comparáveis, o resultado é `null`; não significa consistência comprovada. C0 continua sem receber o alvo de duração e deve ser interpretada dessa forma.
- O nível escolar mantém a correspondência lexical e acrescenta um alerta de menção a ensino médio/fundamental. Esse alerta não mede adequação à faixa etária nem identifica automaticamente o público-alvo.

## Verificação

```bash
python -m unittest discover -s tests -p 'test_automatic_metrics*.py'
python -m unittest discover -s tests -p test_pilot_metrics_audit.py
```

Os testes v2 usam uma tarefa sintética de grafos, duração de 40 minutos, recursos e metodologia diferentes dos exemplos do piloto. Verificam os sete resultados em cinco representações do mesmo conteúdo, evidências originais, limites de seção, rótulos desconhecidos, negação, categoria não funcional, durações compostas, ausência de dados, níveis mistos e separação entre versões. As mudanças de formatação podem alterar números de linha e evidências, mas devem preservar os estados dos requisitos nos formatos suportados.

## Limites e próxima etapa

Não há garantia para toda formatação possível: tabelas HTML/Markdown, rótulos arbitrários, palavras por extenso e paráfrases não estão cobertos. Cronogramas por etapas em minutos não são somados; apenas intervalos HH:MM contíguos são extraídos. Títulos aninhados não reconhecidos e negação complexa ainda podem causar incertezas ou erros. Verbos, conceitos e aliases são proxies textuais, sem validação semântica, factual ou pedagógica. Não há nota composta.

A reanálise agora pode ser executada explicitamente, preservando os arquivos v1:

```powershell
.\.venv\Scripts\python.exe scripts/evaluate_pilot.py artifacts/pilot-qwen3-local --version v2
.\.venv\Scripts\python.exe scripts/summarize_local_pilot.py artifacts/pilot-qwen3-local
```

O primeiro comando grava `automatic_metrics.v2.json`. O segundo reproduz e confere as duas versões antes de consolidar `analysis.v2.json`, `ANALYSIS_V2.md` e `requirements.v1-v2.csv`; separa também as verificações pendentes em `review_cases.v2.json`. Ele prepara a fila de julgamento offline, sem enviar solicitações a fornecedores. A reanálise está identificada como exploratória. Os hashes dos códigos, esquema, configuração e log ficam no relatório consolidado, sem adicionar outro manifesto experimental.

`judge_queue.jsonl` contém somente prompts e identificadores opacos; `judge_mapping.jsonl` contém o vínculo com as gerações e repetições. Apenas os prompts devem ser enviados à julgadora; o mapeamento é reservado à análise. O modelo e seus parâmetros continuam definidos na configuração única do piloto. Esta preparação não verifica saldo, disponibilidade do modelo julgador ou custo de execução. Nenhum julgamento semântico foi realizado.

As regras devem ser congeladas antes da coleta principal. As 24 verificações C1/C2 pendentes neste piloto devem ser interpretadas como incertezas/ausências lexicais do extrator, sem ajuste retrospectivo para maximizar correspondências.

## Estado verificado em 17/10/2026

- Reanálise concluída sobre as mesmas 27 respostas: 189 verificações e 63 agrupamentos por tarefa, condição e requisito. Houve 50 mudanças de estado entre v1 e v2.
- 81 prompts de julgamento preparados e vinculados ao log, sem execução de julgamentos. O teste confere unicidade, hashes e ausência dos identificadores de geração nos prompts.
- Consolidação reproduzível: os testes verificam que os arquivos originais permanecem inalterados, detectam métricas modificadas e rejeitam resultados duplicados.
- Suíte completa no ambiente virtual Windows: 159 testes, todos aprovados. Foram explicitadas leituras UTF-8 e corrigida uma suposição de teste sobre a permanência do arquivo de lock após liberação no Windows; o mecanismo de bloqueio da aplicação não foi alterado.
- Ambiente virtual Windows alinhado aos pins existentes: `google-genai==1.56.0` e `google-auth==2.45.0`. Isso corrige compatibilidade local do SDK; não confirma acesso de geração ou faturamento Google.

O relatório principal desta etapa está em `artifacts/pilot-qwen3-local/ANALYSIS_V2.md`. A comparação Gemini e a avaliação semântica continuam pendentes. Os resultados continuam exploratórios e não demonstram superioridade de uma condição.
