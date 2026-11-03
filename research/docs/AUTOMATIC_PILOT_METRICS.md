# Métricas automáticas do piloto

Implementação: `src/experiment/automatic_metrics.py`, versão
`eduadocs-textual-proxies-v1`. Não utiliza LLM, chamadas externas ou nota composta.
As âncoras são lidas de `experiments/pilot_config.json`, sem modificar os textos gerados.

## Medidas implementadas

- Número de palavras por tokenização simples com expressão regular.
- Evidências textuais dos sete requisitos: tema e nível no texto; verbos/conceitos em
  objetivos; metodologia; recursos; ações avaliativas nas respectivas seções reconhecidas.
- Cada grupo de aliases guarda linha, trecho, alias encontrado e contexto ambíguo.
- Normalização de caixa/acentos, respeitando limites de palavras. “Não funcionais” não
  conta automaticamente como evidência separada de “funcionais”.
- Contexto potencialmente negado é sinalizado e não basta para evidência positiva.
- Duração declarada em minutos/horas, inclusive em linha seguinte ao rótulo.
- Soma de intervalos HH:MM contíguos, com indicação de divergência em relação ao alvo.
- Preservação das medidas operacionais já fornecidas: latência, tokens e término.

`present=true` significa somente que todos os grupos lexicais têm ocorrências positivas.
`false` significa que a busca não encontrou todos os grupos em texto/seção reconhecidos;
não comprova ausência semântica. `null` indica seção não reconhecida ou ambiguidade.
Não há escala 0/0,5/1 nem soma dos sete requisitos.

## Limites dos extratores

Cabeçalhos fora dos padrões reconhecidos e paráfrases podem produzir falsos negativos.
A detecção de negação é heurística e conservadora, não uma análise linguística completa.
Os aliases do nível indicam ensino superior, sem garantir formação introdutória em CC.
Há distinção entre localizar objetivos e avaliar se eles são pedagogicamente adequados.

Para duração, o programa ainda não soma etapas expressas apenas como “atividade: 10 min”,
tabelas arbitrárias, valores por extenso, intervalos sobrepostos ou cronogramas duplicados.
Nesses casos, a soma fica nula. A ausência de contradição detectada não equivale a prova
de consistência. A extração de um cronograma contíguo tampouco demonstra que nenhuma etapa
ficou fora do texto reconhecido. Índices de legibilidade, classificação automática de
idioma, correção factual/algorítmica e avaliação semântica não foram implementados aqui.

## Aplicação aos textos preliminares

```powershell
python scripts/evaluate_preliminary_plans.py
```

Resultado: `artifacts/preliminary_automatic_metrics.json`. São três observações técnicas,
não amostras do piloto: uma do Qwen3 e duas do Llama 3. Foram excluídas a sondagem com
problema de codificação e a resposta Google de teste de conexão.

No Qwen3, foi detectada duração declarada de 50 minutos e cronograma de 60. Nos dois
textos Llama 3, o término por limite (`length`) permanece explícito, e não houve soma
de cronograma identificável. Não comparar qualidade entre essas observações, pois os
prompts e os limites de geração foram diferentes.

O custo permanece nulo, sem preços ou consumo estimados silenciosamente. O relatório
não agrega falhas técnicas como notas zero. A ligação dessas funções aos resultados
das 54 gerações poderá ser feita depois, sem gerar novamente as respostas.

## Verificação

```powershell
python -m unittest tests.test_automatic_metrics -v
```

Casos cobrem contradição 50/60, normalização de horas, ausência de dados, intervalos
sobrepostos, negação, categorias funcionais/não funcionais, escopo de seção, texto vazio
e a resposta Qwen3 preservada. São testes dos extratores; não validação científica da
qualidade pedagógica ou da confiabilidade semântica dos indicadores.
