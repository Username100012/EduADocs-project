# Comparação exploratória da julgadora Sol

Autorizada em 19/10/2026 para verificar a troca de julgadora, sem refazer os 81 julgamentos do piloto. A configuração ativa e os seis artefatos metodológicos congelados não são alterados.

## Documentação consultada

- [Modelo GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol): identificador publicado, saída estruturada, Responses API e raciocínio obrigatório (`low`, `medium`, `high`, `xhigh`, `max`; `none` não suportado).
- [Preços](https://developers.openai.com/api/docs/pricing), consulta em 19/10/2026: Standard, contexto curto, por milhão de tokens: entrada US$ 2; entrada em cache US$ 0,10; escrita de cache US$ 2,50; saída US$ 10. Mini: entrada US$ 0,75; entrada em cache US$ 0,075; saída US$ 4,50. Estimativas na data de referência, não faturas históricas.

## Controles e diferenças

Os mesmos candidatos, payloads, IDs opacos, prompts, rubrica, esquema, três repetições e ordem de execução do diagnóstico Mini são reutilizados. Os hashes e textos são conferidos automaticamente. O Sol grava um diretório separado; a comparação lê os relatórios anteriores sem regravá-los.

Não é uma comparação causal de modelo isolado. Além do modelo, parâmetros precisam diferir:

| Parâmetro | Mini anterior | Sol |
|---|---|---|
| Modelo | gpt-5.4-mini-2026-03-17 | gpt-6.1-sol |
| Raciocínio | none | low |
| Temperatura | 0 | omitida |
| top_p | 1 | omitido |
| Limite de saída, incluindo raciocínio | 1200 | 4096 |
| Formato | JSON com esquema estrito | mesmo esquema |
| Histórico/ferramentas | ausentes | ausentes |
| store | false | false |
| Tier | standard (transporte default) | mesmo |

O limite de saída foi ampliado previamente para acomodar raciocínio e evitar truncamento por um limite destinado à configuração sem raciocínio. Não se presume igualdade de orçamento computacional. Os parâmetros omitidos não podem ser descritos como zero. A página consultada não apresenta snapshot datado para o Sol; preservar metadados retornados e não alegar versão imutável.

## Execução

```powershell
.\.venv\Scripts\python.exe scripts/check_sol_access.py
.\.venv\Scripts\python.exe scripts/run_judge_sensitivity.py --output artifacts/judge-sensitivity-sol-v1 --model gpt-6.1-sol --live
.\.venv\Scripts\python.exe scripts/run_judge_sensitivity.py --output artifacts/judge-sensitivity-sol-v1 --model gpt-6.1-sol --summarize
.\.venv\Scripts\python.exe scripts/compare_judge_sensitivity.py artifacts/judge-sensitivity-v1 artifacts/judge-sensitivity-sol-v1
```

O primeiro comando realiza uma chamada técnica separada e não deve ser repetido desnecessariamente. O executor conserva bloqueio, persistência append-only, zero tentativas automáticas e bloqueio de retomada após início sem resultado. O consolidado só compara lotes completos de 36 respostas válidas.

O teste técnico confirmou acesso ao modelo e JSON aceito pelo parser local, com 1188 tokens de entrada (1185 de escrita de cache) e 319 de saída, em 10,66 s. Pelas tarifas consultadas, a estimativa é US$ 0,00616 para esse teste; extrapolar para 36 produz aproximadamente US$ 0,22, sem constituir garantia de custo. Consumo e cache efetivos do lote são tratados no relatório final. O pré-teste não entra na comparação.

## Alcance

Os três casos reutilizam tarefas do piloto e defeitos evidentes. Uma eventual melhora é indício exploratório neste conjunto; não valida confiabilidade geral, não prova eficácia pedagógica e não justifica substituir notas antigas. A seleção definitiva deve considerar sensibilidade, estabilidade, custo e casos novos reservados, sem ajustar a rubrica para favorecer uma condição de prompt.

## Resultado concluído em 19/10/2026

Foram concluídos 36/36 julgamentos válidos no Sol. Nas nove comparações houve queda estrita no critério-alvo: fidelidade 4→3 na omissão, alinhamento 4→2 no desalinhamento e coerência/exequibilidade 4→2 na contradição temporal, nas três tarefas. O Mini havia apresentado seis quedas e três empates, estes na omissão.

Concordância exata em trincas por texto/critério: Sol 44/48, Mini 40/48. As repetições não são amostras independentes. A intensidade da penalidade não é, por si só, evidência de maior acerto; o diagnóstico relevante é a resposta à perturbação prevista.

Sol: 42.766 tokens de entrada, 11.580 de saída; latência mediana 7,99 s; estimativa Standard US$ 0,2227 com escrita/leitura de cache efetivamente informadas. Mini: 42.766 de entrada, 10.051 de saída; mediana 2,30 s; estimativa às tarifas consultadas US$ 0,0773. Não são comprovantes de cobrança. O pré-teste Sol é separado.

O resultado favorece a configuração Sol para sensibilidade aos defeitos deste conjunto, mas a mudança de raciocínio e amostragem impede atribuir o efeito apenas ao modelo. O próximo passo é confirmar o comportamento em casos novos reservados antes da seleção definitiva; não foram refeitos os 81 julgamentos do piloto nem alterado o modelo ativo. A suíte completa no Windows passou com 174 testes.

Relatórios: `artifacts/judge-sensitivity-sol-v1/COMPARISON.md`, `comparison.json`, `RESULTS.md`, `report.json` e `judgments.jsonl`.
