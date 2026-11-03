# Execução do piloto de 54 gerações

O executor lê `experiments/pilot_config.json`, prepara as 54 solicitações e usa os
construtores C0/C1/C2 existentes. Não aplica métricas nem chama a julgadora.

São 27 solicitações por gerador: Gemini e Qwen3 4B Q4_K_M. Os IDs incluem o gerador;
as respostas de modelos diferentes não se confundem durante a retomada. Os prompts
de uma tarefa/condição são os mesmos nos dois geradores, com o mesmo payload em C1/C2.
Cada gerador usa parâmetros próprios, constantes entre as três condições. Temperatura
e seed não têm equivalência garantida entre fornecedores.

O Qwen3 usa contexto 8192, saída máxima 4096, temperatura 0,7, seed 42, think=false e
keep_alive=10m. O timeout local é 600 segundos. Seed fixa pode resultar em repetições
idênticas; isso é reportado como estabilidade, não como independência estatística.

Na raiz do projeto, em PowerShell, primeiro teste sem custo:

```powershell
python scripts/run_pilot.py --output artifacts/pilot-simulado-54
```

Para a coleta real, com dependências atualizadas e chave Google no ambiente ou `.env`:

```powershell
python scripts/run_pilot.py --live --output artifacts/pilot-real-54-001
```

O mesmo comando retoma a pasta existente. Não misturar simulação e coleta na mesma
pasta. A coleta real não foi executada nesta integração. O Ollama precisa estar em
execução no endereço definido na configuração. Antes da primeira chamada, verificam-se
o digest do Qwen3 instalado e a versão do Ollama. Falha nessa verificação interrompe a
operação; o executor não baixa nem atualiza modelos.

Pastas antigas com 27 solicitações permanecem intactas e não aceitam retomada com a
configuração nova. Para a execução no WSL, localhost pode não apontar ao Ollama do
Windows; preferir rodar o script no PowerShell do Windows. Não mudar host no meio da
coleta sem tratar isso como mudança da configuração.

## Registro e retomada

Um único `generations.jsonl` guarda primeiro a configuração completa e os prompts
na ordem sorteada com seed 42, incluindo os dois geradores. Cada solicitação tem identificador estável e dois eventos:
iniciada e resultado. A escrita é sincronizada após cada evento, sob bloqueio exclusivo
da execução. Os resultados preservam texto, término, tokens, latência e versão disponível.

Sucessos e falhas concluídos são pulados na retomada. Erros não são substituídos por
novas respostas. O SDK Google recebe uma tentativa por chamada e timeout de 60 segundos.
Falhas com códigos 401/403/404/429 interrompem a execução para investigação; não mudar
modelo silenciosamente. Outras falhas são registradas e o executor prossegue.

Uma chamada iniciada sem resultado bloqueia retomada automática: não é possível garantir
exatamente uma execução remota após uma interrupção. O registro pendente precisa ser
investigado antes de decidir uma nova chamada. Logs incompletos ou com sequências
inválidas também bloqueiam a retomada, sem correção automática.

Qualquer mudança na configuração ou nos prompts produzidos impede reutilizar a pasta.
O executor verifica que os parâmetros do adaptador correspondem aos do arquivo único.
Não acrescenta requisitos pedagógicos ou esquema obrigatório à saída do gerador.

Respostas com término diferente de STOP/stop são preservadas com status `non_stop`; o
executor não declara que toda resposta STOP tem qualidade válida. Recusas textuais,
idioma e requisitos precisam ser avaliados na próxima etapa. Custos ainda não são
calculados. Falhas de transporte podem não fornecer tokens ou resposta bruta recuperável.

## Verificação local

```powershell
python -m unittest tests.test_pilot_runner tests.test_google_pilot_adapter tests.test_ollama_pilot_adapter -v
```

Os testes verificam 54 solicitações únicas, 27 por gerador, plano reproduzível,
roteamento de adaptadores, opções locais, digest, retomada sem duplicação, preservação
de falhas/truncamentos, bloqueio após interrupção e mudanças de configuração.
