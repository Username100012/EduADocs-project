# Viabilidade local — inspeção em 15/10/2026

Ollama instalado no Windows: 0.17.1. Inventário observado:

| Tag instalada | ID curto | Tamanho em disco informado |
|---|---|---|
| llama3.2:latest | a80c4f17acd5 | 2,0 GB |
| phi3:mini | 4f2222927938 | 2,2 GB |
| llama3:latest | 365c0bd3c000 | 4,7 GB |

Foi escolhido para uma sondagem técnica o `llama3:latest`, 8,0B, GGUF Q4_0.
Digest completo:
`365c0bd3c000a25d28ddbf732fe1c6add414de7275464c4e4d1c3b5fcb5d8ad1`.
O alias latest sozinho não identifica os pesos para uma coleta científica.

O hardware consultado é i7-10870H, aproximadamente 64 GB de RAM física e RTX 2060 de
6 GB. O candidato foi escolhido entre modelos já instalados para verificar uso real
da GPU, sem baixar novos pesos. Isso não é uma comparação de qualidade com os outros
modelos nem demonstra que seja o melhor modelo disponível para português ou Computação.

## Procedimento

O script `scripts/check_ollama_local.ps1` faz duas chamadas locais, com a primeira tarefa
de programação e um prompt semelhante a C1. Temperatura 0,7, seed 42, contexto 4096,
limite de 512 tokens de saída, retenção em memória de 10 minutos. As respostas são
rascunhos técnicos fora do conjunto experimental.

As medições incluem duração total observada, carregamento, contagem e tempo dos tokens,
estado `/api/ps`, VRAM global da GPU e working set/memória privada dos processos Ollama.
O estado da memória é amostrado após cada chamada: não é pico de consumo. Working set
e memória privada não são intercambiáveis nem somáveis como consumo físico exclusivo.

Foi preservada uma primeira sondagem com problema de codificação dos acentos do script
em `artifacts/ollama_local_feasibility_encoding_issue.json`. O script recebeu BOM UTF-8
para Windows PowerShell e foi novamente executado. O relatório corrente é
`artifacts/ollama_local_feasibility.json`. O modelo já estava carregado na repetição
do script; o rótulo initial_load significa primeira chamada do script, não garante cache
frio. Conferir load_duration e estado do serviço ao interpretar os tempos.

## Interpretação

A sondagem confirma que o modelo instalado pode gerar texto com aceleração na GPU.
A distribuição de memória informada pelo Ollama não justifica afirmar execução
integral em GPU. As respostas limitadas a 512 tokens terminam por comprimento, não
demonstram conclusão de um plano de aula completo. Antes de adotar este candidato no
piloto será necessário testar o contexto e o limite de saída efetivos do experimento,
definir a versão dos pesos e adaptar o executor, atualmente restrito ao Google.

Duas chamadas não estimam de forma robusta média, variância, consumo de pico ou latência
para as três tarefas. Não foi feito experimento CPU versus GPU.

Referências técnicas:
[generate](https://docs.ollama.com/api/generate) e
[modelos carregados](https://docs.ollama.com/api/ps).
