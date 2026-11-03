# Fechamento operacional do piloto v2 — 25/10/2026

Objetivo: concluir uma rodada delimitada sobre os 27 planos já salvos, sem novas gerações, mudança de modelo/rubrica ou otimização de prompts após resultados.

## Diagnóstico separado

Um plano sintético novo de fila FIFO, fora do catálogo de coleta, foi preparado em seis versões: base, formatação, verbosidade, omissão de materiais, avaliação desalinhada e duração contraditória. Cada versão recebe três julgamentos. A definição e as expectativas foram gravadas antes das chamadas em `artifacts/reserved-requirement-v2/reserved_manifest.json`; não são mostradas à julgadora. O executor reconstrói o manifesto antes da execução e recusa divergências.

As 18 respostas passaram pelo contrato e as seis relações previstas foram satisfeitas. Trata-se de diagnóstico autoral com um tópico e defeitos explícitos, não benchmark validado nem acurácia geral. Os casos foram inspecionados no desenvolvimento do software: “reservado” significa não usado para ajustar o contrato antes desta rodada, não um conjunto independente cegado por terceiros.

## Mudanças operacionais, sem alterar o contrato

Paralelismo limitado a seis chamadas por onda para reduzir tempo de execução. Registro de início/resultado continua exclusivo de um escritor, com bloqueio e fsync. Após falha, chamadas já iniciadas são concluídas e registradas. Sem tentativas automáticas. A concorrência fica registrada por chamada; latências de julgamento não devem ser comparadas como se toda a execução fosse sequencial.

O lote parou inicialmente após um `evidence_mismatch`: a citação de materiais perdeu espaços finais na última linha. A rejeição é mantida: o contrato exige igualdade literal e não será afrouxado. Após inspeção, decidiu-se terminar os itens ainda não chamados com `--continue-validation-errors`: erros de validação permanecem falhas, sem reparo, reenvio ou zero; erros de transporte/API/modelo ou respostas incompletas continuam interrompendo novas ondas. Esta mudança de política operacional é posterior à primeira falha e deve ser declarada; não altera a mensuração.

## Recuperação restrita de autenticação

Há dois erros HTTP 401 anteriores à correção da precedência da chave. Não houve resposta de modelo nesses dois casos. Foi definida uma única recuperação manual em log separado, somente para esses IDs, com as mesmas requisições, modelo e parâmetros. Nenhuma falha semântica, de citação ou de validação é elegível. `scripts/recover_requirement_auth_failures.py` verifica os dois erros históricos e mantém todos os registros originais. A agregação deve distinguir tentativas operacionais de avaliações válidas únicas, sem duplicar IDs recuperados.

## Saídas

- `artifacts/reserved-requirement-v2/relations_report.json`: diagnóstico.
- `artifacts/judge-contract-v2-preparation/judgments.v2.jsonl`: tentativas do lote, sem alteração do histórico.
- `scripts/report_requirement_results.py`: tabelas descritivas por requisito e condição, denominadores e trincas completas; sem score composto ou significância.
- A coleta principal de 12 tarefas e dois geradores continua em rascunho; este fechamento não representa sua execução.

## Encerramento

O lote foi concluído: 81 avaliações únicas, 80 julgamentos válidos e uma falha de citação preservada. Houve 83 tentativas operacionais no total, incluindo os dois erros históricos 401 e suas duas recuperações manuais. C0: 27/27 válidos, nove trincas completas; C1: 26/27 válidos, oito trincas completas; C2: 27/27 válidos, nove trincas completas.

As 80 respostas brutas válidas foram reprocessadas pelo parser, sem divergência dos resultados salvos; a falha de citação foi reproduzida. A soma específica de seis etapas de um plano C1 foi verificada computacionalmente como 65 minutos, contra alvo de 50. Essas verificações estão em `artifacts/judge-contract-v2-preparation/evidence_audit.json` e não comprovam o acerto das demais classificações semânticas.

Os resultados não favorecem C2 em todos os critérios: as medianas entre tarefas foram 4/4 para alinhamento em C1/C2 e 4/3 para coerência textual. As distribuições nominais são estimativas da julgadora; não são acurácia ou qualidade pedagógica comprovada. Nenhuma nova chamada foi feita para corrigir esse resultado.

O [texto-base para o artigo](ARTICLE_COMPUTATIONAL_PILOT_V2.md) e as tabelas completas estão prontos para revisão dos autores. Permanecem fora destes resultados o estudo principal, a comparação com Gemini e a avaliação dos outros tipos de material.
