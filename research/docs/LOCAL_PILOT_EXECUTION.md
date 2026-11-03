# Piloto local Qwen3

Execução local separada porque o acesso faturado ao Gemini ainda não foi resolvido. Não há chamadas ao Google nem à julgadora OpenAI nesta etapa.

O executor usa o mesmo `experiments/pilot_config.json`, valida o plano completo e filtra os 27 trabalhos do Qwen3 após o embaralhamento original. Preserva identificadores, prompts, payloads e parâmetros; não altera o protocolo para remover o Gemini. O cabeçalho do JSONL armazena a configuração completa e os trabalhos efetivamente selecionados. Assim, esta etapa representa somente a parcela local do piloto, não a comparação entre geradores.

## Executar no PowerShell, na raiz do projeto

```powershell
.\.venv\Scripts\python.exe scripts/run_pilot.py --live --generator qwen3 --output artifacts/pilot-qwen3-local
```

`--live` significa geração real; com `--generator qwen3`, somente o Ollama local é usado e não é exigida chave Google. Sem `--live`, a execução é simulada. O Ollama precisa estar iniciado, com versão e digest previstos na configuração. A configuração contém três tarefas, três condições e três repetições, totalizando 27 respostas locais. Seed fixa: repetições não são amostras independentes.

Os registros são persistidos após cada início e resultado em `artifacts/pilot-qwen3-local/generations.jsonl`. A retomada com o mesmo comando não repete resultados já registrados, incluindo falhas. Um início sem resultado bloqueia a retomada para investigação, evitando duplicação silenciosa. Não apague o registro para contornar esse bloqueio.

## Análise sem novas gerações

```powershell
.\.venv\Scripts\python.exe scripts/evaluate_pilot.py artifacts/pilot-qwen3-local
```

O relatório `automatic_metrics.json` deriva dos textos originais, preserva erros e truncamentos e inclui hashes do log e da configuração. As métricas são as mesmas proxies textuais já implementadas; não validam correção factual, qualidade pedagógica ou eficácia de ensino. A ausência de correspondência lexical não comprova ausência semântica. O relatório pode ser calculado durante a coleta, mas será parcial até os 27 resultados estarem registrados.

Não misturar este diretório com uma execução dos dois geradores: a seleção faz parte do cabeçalho validado. Uma futura coleta Gemini deve usar outro diretório e o mesmo arquivo de configuração, se os controles permanecerem válidos.
