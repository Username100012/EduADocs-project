# Seleção técnica do modelo julgador

## Decisão

O julgador principal do experimento será o snapshot
`gpt-5.4-mini-2026-03-17`, acessado pela API Responses da OpenAI.

Configuração a ser congelada no manifesto:

```text
provider: openai
model: gpt-5.4-mini-2026-03-17
model_version: gpt-5.4-mini-2026-03-17
api: responses
response_format: json_schema (strict)
reasoning_effort: none
temperature: 0
top_p: 1
seed: null
max_output_tokens: 1200
store: false
service_tier: standard
```

O snapshot datado será usado tanto em `model` quanto em `model_version`; o alias móvel
`gpt-5.4-mini` não será usado na coleta experimental.

## Critérios

### Saída estruturada

O modelo oferece Structured Outputs. A chamada deverá fornecer diretamente o esquema
`experiments/llm_judge_response.schema.json` com validação estrita. O parser local
continuará obrigatório como verificação independente da resposta recebida.

### Reprodutibilidade

A documentação oficial publica o snapshot `gpt-5.4-mini-2026-03-17` e informa que
snapshots fixam uma versão específica para manter comportamento consistente. Essa
propriedade é superior, para este experimento, ao uso de aliases estáveis sem data.

### Custo

Na consulta realizada em 15 de outubro de 2026, a documentação oficial informava preços
standard de US$ 0,75 por milhão de tokens de entrada e US$ 4,50 por milhão de tokens de
saída. O custo real será calculado a partir dos tokens registrados; estimativas não serão
substituídas por valores observados.

### Capacidade

O julgamento é uma tarefa curta, pointwise, com quatro critérios e esquema explícito.
Assim, o modelo mini representa melhor equilíbrio entre capacidade e custo do que o
modelo flagship. `reasoning_effort=none` evita tokens de raciocínio variáveis e permite
fixar os parâmetros de amostragem definidos no protocolo.

### Independência

O snapshot escolhido não integra atualmente as opções de geração do EduADocs. Isso evita
que o mesmo modelo exato gere e julgue os materiais. A independência, porém, não é total:
alguns geradores pertencem à OpenAI, podendo existir viés de família ou fornecedor.
Consequentemente:

- identidade do gerador e condição permanecerão ocultas do julgador;
- métricas determinísticas continuarão sendo o desfecho principal;
- notas do julgador serão secundárias;
- resultados de saídas OpenAI deverão ser apresentados separadamente por modelo;
- um segundo julgador de outro fornecedor poderá compor análise de sensibilidade, mas
  não será misturado ao desfecho principal.

## Alternativas rejeitadas

### GPT-4.1

Embora possua saída estruturada e snapshot datado, a documentação atual o classifica como
deprecated. Não é adequado iniciar uma nova coleta com esse modelo.

### GPT-6 Astra

Possui maior capacidade, mas o custo é desproporcional para uma rubrica curta e seu uso
não elimina os vieses próprios de LLM-as-a-judge. Maior capacidade não garante validade
pedagógica.

### Gemini 2.5 Pro

Suporta saídas estruturadas, porém já aparece entre os geradores do EduADocs. Além disso,
a página oficial consultada apresenta `gemini-2.5-pro` como versão estável, sem snapshot
datado equivalente na mesma página, e recomenda modelos mais recentes para novos
projetos. Isso reduz independência e reprodutibilidade para o papel de julgador principal.

## Fontes oficiais consultadas

- OpenAI, GPT-5.4 Mini Model:
  https://developers.openai.com/api/docs/models/gpt-5.4-mini
- OpenAI, Structured model outputs:
  https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI, API deployment checklist:
  https://developers.openai.com/api/docs/guides/deployment-checklist
- Google, Gemini 2.5 Pro:
  https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro

