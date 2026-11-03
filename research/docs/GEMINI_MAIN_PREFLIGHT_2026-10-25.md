# Verificação de acesso ao Gemini — 25/10/2026

Foi testado o modelo `gemini-3.8-flash` e sua configuração em `experiments/main_config.json`, fora da coleta experimental. Consulta de metadados e uma única tentativa de geração mínima (`Responda somente: OK`), sem tentativas automáticas e sem alterar modelo, limites ou parâmetros.

Resultado da geração: HTTP **402**, `RESOURCE_EXHAUSTED`, com a mensagem **Your prepayment credits are depleted**. O serviço informa esgotamento de créditos pré-pagos. Isso impede iniciar a coleta; não é uma falha de prompt ou indicação de que seja necessário trocar de modelo.

O diagnóstico sanitizado foi preservado em `artifacts/gemini-main-preflight-2026-10-25.json`. Não foram gerados planos nem iniciada a coleta principal. A consulta de inferência não informa saldo numérico, preço efetivamente cobrado ou detalhes completos da conta de faturamento.

## Ação necessária

No Google AI Studio, selecionar o projeto correspondente à chave do `.env`, abrir Billing e consultar o saldo disponível. Para conta Prepay esgotada, adicionar créditos pela opção Buy credits. Nenhuma alteração de faturamento, compra ou recarga automática foi realizada pelo assistente.

A [documentação oficial de faturamento](https://ai.google.dev/gemini-api/docs/billing#prepay) informa que o esgotamento do saldo Prepay causa HTTP 402 até que novos créditos sejam adicionados. Conferir projeto e conta de faturamento na interface, pois uma chave de inferência não fornece acesso administrativo a esses dados.

Após regularizar o saldo, repetir somente o preflight mínimo. Com geração bem-sucedida, revisar e congelar o protocolo em etapa separada, mantendo o piloto fora da coleta principal. A configuração principal permanece `draft_offline_only`.

## Ajuste de credenciais

Os três comandos experimentais Google (`check_google_pilot.py`, `diagnose_google_access.py`, `run_pilot.py`) passaram a compartilhar `google_credentials.read_google_key`: primeiro as entradas não vazias do `.env` do projeto, priorizando GOOGLE_API_KEY sobre GEMINI_API_KEY; depois as variáveis do processo. Nenhuma variável global do Windows foi alterada, nenhuma credencial foi impressa e os artefatos metodológicos congelados permaneceram intactos.

Repetição segura e delimitada:

```powershell
.\.venv\Scripts\python.exe scripts/diagnose_google_access.py --config experiments/main_config.json --output artifacts/gemini-main-preflight-after-credit.json --skip-list
```

Esse comando consulta o modelo e tenta uma geração mínima; não inicia o estudo principal.

Validação local: suíte completa com 202 testes aprovados no Windows. A consulta de metadados do modelo foi bem-sucedida; a geração foi a única operação recusada por saldo.

## Repetição após regularização de créditos

A nova consulta e a geração mínima foram bem-sucedidas: `gemini-3.8-flash` respondeu `OK`, com 7 tokens de entrada e 1 de saída. Registro: `artifacts/gemini-main-preflight-after-credit.json`. O bloqueio HTTP 402 não ocorreu nesta tentativa. Isso confirma acesso operacional no momento do teste; não revela saldo numérico nem garante cota suficiente para toda a coleta. A coleta principal não foi iniciada; o protocolo permanece em rascunho até a revisão e o congelamento.
