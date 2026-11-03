# Revisão e congelamento local do estudo principal — 25/10/2026

Versão: **eduadocs-main-v1.0.0**. Configuração única: `experiments/main_config.json`. Selo SHA-256 do arquivo: `experiments/main_config.json.sha256`.

SHA-256 final da configuração: `b0ec9b311a388756ec4fe9591654b8a6c975795fdc8986a210e9e994f173abc3`.

## Decisões fechadas

- Doze tarefas, quatro por área; três condições; três repetições; dois geradores: 216 gerações e até 648 julgamentos elegíveis.
- Comparação principal C1/C2 dentro de tarefa e gerador. C0 é controle com informação reduzida, não uma ablação isolada de estrutura.
- Os sete valores do payload e todos os 216 itens do plano de geração são idênticos ao planejamento anterior à revisão. Metadados de pré-requisitos e limites não são enviados às LLMs.
- Observações sintáticas são separadas de estimativas semânticas; o extrator temporal congelado não soma títulos arbitrários de etapas. Foram removidas instruções contraditórias que prometiam essa soma ou descreviam os estados antigos como medida principal.
- Julgadora v2, cinco categorias nominais por requisito, evidências literais e duas notas autorais. Sem nota composta, voto majoritário, significância, eficácia educacional ou validação humana.
- Três julgamentos por resposta STOP/stop válida. Outputs truncados ficam identificados nos indicadores primários; não entram nos julgamentos secundários.
- Geração sequencial; julgamento com seis chamadas simultâneas por onda. Erros de validação permanecem falhas, sem reparo ou repetição; erros operacionais interrompem novas ondas.
- As análises ficam estratificadas por gerador, tarefa e condição. Corrigida a consolidação que antes pressupunha apenas um gerador, preservando a interpretação do piloto de Qwen3.

## Integridade e histórico

O selo verifica a configuração, os hashes de 33 artefatos definidores, o catálogo e o plano dos prompts antes de chamadas reais. Alterações bloqueiam a execução. É um registro local anterior à coleta principal, informado pelos pilotos; não é pré-registro externo ou garantia de imutabilidade dos modelos hospedados.

O snapshot integral da configuração usada nos julgamentos do piloto foi incorporado ao relatório de proveniência existente (`preparation_report.json`), sem alterar prompts, IDs ou logs executados. Assim, o novo status/configuração principal não invalida a reconstrução do piloto. A rodada diagnóstica anterior também mantém seu manifesto e seus IDs originais. Não foi criada uma segunda configuração ativa.

A preparação regenerada está em `artifacts/main-preparation/`. Ela contém somente planos e verificações locais, não respostas experimentais. O orçamento original de R$ 12,52 continua aplicável porque o modelo, os parâmetros e todos os textos dos prompts foram preservados; R$ 30 é referência flexível e o saldo OpenAI é separado.

## Verificações

- Suíte Windows: 209 testes aprovados antes do selo; conferência final do mesmo selo no Windows bem-sucedida.
- Simulação temporária: 216 respostas fictícias e fila de 648 julgamentos, sem rede; testes garantem identificação de simulação e bloqueio de seu uso como coleta real.
- Testes de configuração sem selo e deriva de fontes; teste de agregação separada de Gemini e Qwen3.
- Reconstrução da fila anterior de 81 julgamentos e dos 18 casos diagnósticos preservada.
- Hashes dos logs originais conferidos sem alteração.
- Zero chamadas de geração ou julgamento nesta revisão; coleta principal não iniciada.

## Próximo passo

Iniciar a coleta em diretório novo com o comando do [protocolo congelado](MAIN_STUDY_PROTOCOL.md). O executor confere SDK Google, versão Ollama e digest local antes das respectivas chamadas; a disponibilidade das contas e do serviço deve persistir na data de execução. Nenhum modelo será baixado ou substituído automaticamente.
