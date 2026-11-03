# Julgamentos principais — execução concluída

**Execução real iniciada em 26/10/2026, retomada e concluída em 27/10/2026: 645 tentativas, 624 julgamentos válidos, 15 falhas de validação e seis erros de saldo preservados da execução anterior. Nenhuma chamada pendente ou repetida.** Estado autoritativo por chamada: `judgments.v2.jsonl`. O executor usa o saldo OpenAI, seis chamadas por onda e a política congelada. A preparação anterior foi exclusivamente offline. A origem são os 215 planos elegíveis da coleta principal, com três repetições por plano. A tentativa Gemini `task-002/C1/r1`, encerrada com ReadTimeout e sem texto, está excluída e continua preservada no log de geração.

| Gerador | Condição | Planos | Julgamentos |
|---|---|---:|---:|
| Gemini | C0 | 36 | 108 |
| Gemini | C1 | 35 | 105 |
| Gemini | C2 | 36 | 108 |
| Qwen3 | C0 | 36 | 108 |
| Qwen3 | C1 | 36 | 108 |
| Qwen3 | C2 | 36 | 108 |
| Total | | 215 | 645 |

## Conferências da preparação (antes da execução)

- 645 evaluation_id únicos, sem colisão com piloto ou rodada diagnóstica.
- Cada plano elegível tem exatamente as repetições 1, 2 e 3; não há planos omitidos ou duplicados.
- Todos os prompts e corpos de requisição foram reconstruídos a partir do payload e texto originais; conferidos hashes de prompt, candidato e payload.
- Configuração congelada: `gpt-6.1-sol`, reasoning low, limite de 4096 tokens, esquema JSON estrito, store false, temperatura/top_p omitidos.
- Gerador, condição, task_id e job_id ficam no mapeamento separado, não como campos explícitos da requisição. O conteúdo ainda pode revelar características da condição; isso não constitui cegamento absoluto.
- O executor congelado validou a fila em modo offline no Windows, sem `--live`.
- No encerramento da preparação não existia `judgments.v2.jsonl`; o arquivo foi criado somente com o início desta execução real.

## Artefatos

- `queue.jsonl`: prompts e requisições para revisão/execução futura.
- `mapping.jsonl`: vínculo separado entre IDs opacos, plano, gerador, condição e repetição.
- `preparation_report.json`: configuração, contrato e proveniência da preparação.
- `queue_validation.json`: resultado da auditoria, distribuição, exclusão e hashes dos três artefatos acima.

Origem: `../main-study-v1/generations.jsonl`, SHA-256 `70969e6fe4df45f92d7dd9605eb68cb90b6dfa9eaa6d0346bb2f1f1a4b5b4135`.

O protocolo prevê até 648 julgamentos quando todas as gerações são elegíveis; o timeout reduz a fila a 645. Ele não recebeu nota zero e não foi substituído. Repetições não são avaliadores humanos ou tarefas independentes.

## Comando da execução autorizada

O comando de execução paga, conforme a política congelada, será:

```powershell
.\.venv\Scripts\python.exe scripts/run_requirement_judgments.py artifacts/main-study-v1 artifacts/main-judgments-v1 --live --max-jobs 645 --workers 6 --continue-validation-errors
```

Ele usa o saldo OpenAI, separado do Gemini. Não alterar a fila depois de iniciar; o executor verifica novamente sua proveniência. Os erros de validação são preservados, sem reparo ou reenvio; erros operacionais impedem novas ondas, conforme o [protocolo](../../docs/MAIN_STUDY_PROTOCOL.md).

## Interrupção de faturamento

HTTP 429, código `credit_balance_exhausted`, tipo `insufficient_quota`: a API informou ausência de créditos. Não foi tratado como um simples limite de velocidade. As seis chamadas da onda já iniciada foram registradas; nenhuma onda nova foi enviada após a falha.

- 72/645 tentativas concluídas: 65 julgamentos válidos, uma falha de citação (`evidence_mismatch`) e seis erros de saldo.
- 573 IDs ainda não enviados; nenhuma chamada pendente ou duplicada.
- Dados de geração, fila, mapeamento e configuração congelada preservados.
- Diagnóstico operacional em `execution_status.json`; nenhuma comparação semântica final foi produzida com esse lote parcial.

É necessário adicionar créditos na conta **API OpenAI**, separada de Gemini e de uma assinatura ChatGPT. A [documentação oficial](https://developers.openai.com/api/docs/guides/spend-limits#restore-api-traffic) orienta adicionar créditos para esse código específico. Nenhuma recarga ou mudança de conta/modelo foi realizada pelo assistente.

Após regularizar o saldo, o mesmo comando pode retomar somente os 573 IDs não executados. As seis falhas por saldo e a falha de citação continuam no conjunto como resultados operacionais; o protocolo não prevê repetição automática desses IDs. Não editar ou reconstruir a fila para contornar essa política.

## Conclusão em 27/10/2026

A retomada processou somente os 573 IDs ainda não enviados. As 645 tentativas estão encerradas: 624 válidas, 15 falhas de validação e seis erros históricos de crédito. Não houve reenvio de IDs, mudança de protocolo ou alteração da fila, mapeamento e gerações originais. Os hashes e a unicidade dos registros foram conferidos; `summary.v2.json` corresponde ao log.

O bloco de interrupção acima registra o histórico, não o estado atual. O estado atual está em `execution_status.json`. Próximo passo: consolidar os julgamentos salvos, mantendo as falhas como dados ausentes, sem atribuir nota zero e sem chamadas adicionais à API.

## Consolidação concluída em 27/10/2026

[Resumo interpretativo](CONSOLIDATION.md), [tabelas completas](RESULTS.md) e [auditoria](consolidation_audit.json). As 624 respostas válidas foram revalidadas; 196/215 planos têm trinca válida. Notas calculadas com peso igual por tarefa e falhas como dados ausentes; nenhuma chamada adicional às APIs.

Análise dos sete requisitos concluída: [comparação C0/C1/C2 e detalhamento C1/C2 por tarefa](REQUIREMENTS_COMPARISON.md), com distribuições nominais completas e denominadores verificados. [CSV C1/C2 por tarefa](c1_c2_requirements_by_task.csv). Sem chamadas novas às APIs ou mudanças no protocolo.

Auditoria computacional exploratória concluída: [casos, evidências e limitações](case-audit/AUDIT.md). Identificados defeitos dos planos, um erro aritmético verificável da julgadora e variação na interpretação de objetivos. Classificações principais preservadas; zero chamadas adicionais às APIs.

Rascunho para o artigo: [Resultados e limitações do estudo principal](../../docs/ARTICLE_MAIN_RESULTS_AND_LIMITATIONS.md), com [tabela integrada](integrated_results.csv) e conferência de fontes em integration_audit.json. Não substitui o texto histórico do piloto. Nenhuma nova API foi chamada.

Análise complementar em 28/10/2026: [sensibilidade com pares completos](paired-complete-sensitivity/RESULTS.md). Fonte bruta, seleção e contagens conferidas independentemente; nenhuma recodificação, reexecução ou API.
