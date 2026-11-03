# Julgamento automático do piloto local

Esta etapa executa os 81 prompts já preparados (27 respostas × três julgamentos), com `gpt-5.4-mini-2026-03-17` e a configuração existente em `experiments/judge_model_selection.v1.json`. Não gera novos planos. O teste técnico de acesso tem identificador distinto e não entra na coleta.

## Execução e retomada no Windows

```powershell
.\.venv\Scripts\python.exe scripts/run_judgments.py artifacts/pilot-qwen3-local --live
.\.venv\Scripts\python.exe scripts/summarize_judgments.py artifacts/pilot-qwen3-local
```

Sem `--live`, o primeiro comando apenas confere o plano, sem chamadas. A chave é lida do ambiente ou `.env`, não registrada. O corpo da requisição contém apenas o prompt com identificador opaco; o mapeamento para tarefa, condição e gerador fica local. Metadados podem ser inferíveis pelo conteúdo: isso não garante cegamento absoluto.

O executor reconstrói cada prompt a partir da resposta original e payload, valida hashes e cobertura completa antes de iniciar. Registra configuração, esquema e corpos exatos no cabeçalho de `judgments.jsonl`. O arquivo é append-only, com bloqueio exclusivo e flush/fsync por evento. Antes de cada chamada registra o início; depois preserva a resposta bruta, status HTTP, tokens, duração, erro e registro tipado existente. JSON válido ainda passa pelo parser local rigoroso.

Reexecutar o comando com os mesmos arquivos não repete resultados já registrados. Início sem resultado bloqueia retomada, pois a chamada pode ter sido processada remotamente. Não apagar eventos para contornar esse bloqueio. Não há tentativas automáticas; erros de autenticação, acesso ou cota interrompem o lote. A API recebe `store=false`, sem ferramentas ou histórico; o nome de tier `standard` da configuração é convertido para o valor de transporte `default`, como no teste técnico.

## Consolidação

- `judgments.jsonl`: registro integral das chamadas; preserva justificativas e respostas brutas.
- `judgment_scores.csv`: quatro notas individuais por julgamento válido (324 previstas se todos forem válidos).
- `judgment_response_medians.csv`: mediana por plano e critério, somente com três julgamentos válidos (108 previstas).
- `judgment_groups.csv`: estatísticas por condição e por tarefa/condição, com concordância exata das trincas e amplitude das notas.
- `judgment_summary.json` e `JUDGMENT_RESULTS.md`: resultados consolidados, completude, tokens e hashes de origem.

Não há nota composta. Primeiro calcula-se a mediana dos três julgamentos de cada plano; depois a mediana entre planos por condição. Mínimo–máximo é dispersão descritiva, não intervalo de confiança. Falhas não recebem zero nem são descartadas da contagem de execuções. Tokens e cache são registrados; custo financeiro não é calculado usando preços não verificados.

As notas são estimativas secundárias de uma LLM, sem validação humana, factual ou de eficácia pedagógica. C0 não recebeu seis dos requisitos-alvo; diferenças para C1/C2 não isolam apenas estrutura do prompt. As repetições de geração com seed fixa e os três julgamentos de uma mesma resposta não são amostras independentes. Não são realizados testes de significância nem alegações de superioridade geral. A comparação com Gemini permanece pendente.

## Coleta concluída em 17/10/2026

Foram concluídos e validados 81/81 julgamentos, sem falhas e sem tentativas adicionais. São 324 notas individuais e 108 medianas por resposta/critério. Concordância exata em 97/108 trincas, com amplitude máxima de um ponto. A alta concordância descreve estabilidade nesta execução, sem demonstrar validade das notas.

Consumo registrado: 175.884 tokens de entrada e 22.794 de saída. As medianas por condição foram C0 = 2/2/2/3 e C1 = C2 = 4/4/4/4 na ordem fidelidade, alinhamento, adequação ao nível e coerência/exequibilidade. Há variação entre planos, apresentada integralmente no relatório; igualdade de medianas não prova equivalência entre condições nem superioridade de C2.

O relatório principal é `artifacts/pilot-qwen3-local/JUDGMENT_RESULTS.md`. A suíte completa no Windows passou com 165 testes, incluindo execução simulada de 81 julgamentos, retomada sem duplicação, bloqueio de chamada interrompida, detecção de prompt alterado e exclusão de trincas incompletas das medianas. Nenhum plano foi gerado novamente.
