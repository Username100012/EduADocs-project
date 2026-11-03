# Rubrica de avaliação computacional do EduADocs

## 1. Escopo

Esta rubrica avalia computacionalmente planos de aula gerados nas condições C0, C1 e
C2. Ela não mede usabilidade, impacto na aprendizagem, satisfação docente ou qualidade
pedagógica integral.

A unidade experimental é a combinação:

```text
tarefa × condição × modelo
```

As repetições de uma mesma combinação são observações dependentes e deverão ser
agregadas antes dos testes inferenciais.

## 2. Requisitos controlados

Cada tarefa possui sete requisitos, todos com peso igual:

1. tópico;
2. nível educacional;
3. objetivo de aprendizagem;
4. duração;
5. metodologia;
6. materiais e recursos;
7. estratégia de avaliação.

Os requisitos-alvo vêm do `LessonPlanSemanticPayload`, não da resposta do modelo. C0 é
avaliada contra o mesmo alvo de C1 e C2, embora receba somente o tópico. Isso permite
separar o efeito da quantidade de informação (C0 × C1) do efeito de sua organização
(C1 × C2).

## 3. Âncoras de avaliação

Cada tarefa deverá definir, antes das execuções, âncoras determinísticas que não serão
enviadas ao modelo:

- termos essenciais do tópico;
- formas equivalentes do nível educacional;
- conceitos e verbos observáveis do objetivo;
- duração exata e unidade;
- nome e aliases da metodologia;
- itens essenciais de materiais;
- termos essenciais da estratégia de avaliação;
- afirmações factuais obrigatórias e afirmações proibidas, quando aplicável.

As âncoras deverão ser congeladas junto ao catálogo. Não poderão ser alteradas depois de
inspecionadas as respostas experimentais.

## 4. Pontuação de cada requisito

Cada requisito recebe uma pontuação determinística:

| Valor | Interpretação |
|---:|---|
| 0 | ausente ou incompatível com o valor solicitado |
| 0,5 | parcialmente representado ou presente sem elementos essenciais |
| 1 | representado de forma completa e compatível com as âncoras |

Regras específicas:

### 4.1 Tópico

- `1`: todos os termos essenciais ou uma expressão equivalente cadastrada aparecem;
- `0,5`: parte dos termos essenciais aparece, com cobertura maior ou igual a 50%;
- `0`: cobertura inferior a 50% ou ocorrência em contexto incompatível.

### 4.2 Nível educacional

- `1`: nível ou alias cadastrado aparece explicitamente;
- `0,5`: não é nomeado, mas há marcador inequívoco da faixa correspondente;
- `0`: ausente ou incompatível.

Inferência baseada apenas em estilo textual não será suficiente para pontuação completa.

### 4.3 Objetivo de aprendizagem

- `1`: há objetivo explícito contendo verbo observável e os conceitos essenciais;
- `0,5`: há objetivo, mas falta verbo observável ou parte dos conceitos essenciais;
- `0`: objetivo ausente, genérico ou incompatível.

### 4.4 Duração

- `1`: duração total exatamente compatível com a solicitada;
- `0,5`: duração não é declarada, mas etapas temporizadas somam o valor solicitado;
- `0`: duração ausente, incompatível ou soma temporal divergente.

Será aplicada tolerância de um minuto apenas para somas decorrentes de divisão das etapas.

### 4.5 Metodologia

- `1`: metodologia ou alias aparece e é associada ao desenvolvimento da aula;
- `0,5`: metodologia é apenas mencionada, sem uso identificável;
- `0`: ausente ou substituída por metodologia incompatível.

### 4.6 Materiais e recursos

- `1`: todos os itens essenciais são mencionados;
- `0,5`: pelo menos metade, mas não todos, são mencionados;
- `0`: menos da metade é mencionada.

Materiais adicionais não reduzem a pontuação, salvo quando contradizem restrições da
tarefa.

### 4.7 Estratégia de avaliação

- `1`: estratégia ou alias aparece com procedimento avaliativo identificável;
- `0,5`: avaliação é mencionada sem procedimento ou apenas parte dos termos essenciais
  aparece;
- `0`: ausente ou incompatível.

## 5. Métricas primárias

Seja `s_i` a pontuação do requisito `i`, com valores 0, 0,5 ou 1.

### 5.1 Requirement Compliance Score — RCS

Proporção de requisitos completamente atendidos:

```text
RCS = quantidade(s_i = 1) / 7
```

### 5.2 Completeness Score — CS

Média das pontuações, preservando atendimento parcial:

```text
CS = soma(s_i) / 7
```

### 5.3 Omission Rate — OR

Proporção de requisitos totalmente ausentes ou incompatíveis:

```text
OR = quantidade(s_i = 0) / 7
```

RCS, CS e OR não devem ser tratados como observações independentes, pois derivam dos
mesmos sete julgamentos.

## 6. Métricas secundárias

### 6.1 Falhas

Cada execução terá exatamente um status:

- sucesso;
- erro de autenticação;
- limite de taxa;
- indisponibilidade do provedor;
- timeout;
- resposta vazia;
- resposta truncada;
- recusa;
- idioma incompatível;
- erro de processamento;
- erro de exportação.

```text
Failure Rate = execuções sem resposta utilizável / execuções planejadas
```

A falha original deverá permanecer registrada mesmo quando houver nova tentativa.

### 6.2 Latência

Tempo entre o envio da solicitação e o recebimento completo da resposta. Serão reportados
mediana, intervalo interquartil, média e desvio padrão. A geração do DOCX não integra a
latência do modelo.

### 6.3 Tokens

Tokens de entrada e saída serão registrados separadamente quando fornecidos pelo
provedor. Valores ausentes não serão estimados silenciosamente e serão apresentados como
dados faltantes.

### 6.4 Custo

O custo será calculado com tabela de preços versionada e datada:

```text
custo = tokens_entrada × preço_entrada + tokens_saída × preço_saída
```

Modelos locais não receberão custo monetário por chamada. Para eles serão registrados
tempo, hardware e, quando disponível, consumo de memória.

### 6.5 Consistência entre repetições

Para cada tarefa, condição e modelo serão calculados:

- proporção de requisitos completos em todas as repetições;
- desvio padrão do CS;
- coeficiente de variação do tamanho da resposta;
- estabilidade do conjunto de seções identificadas.

Similaridade semântica por embeddings não integra a métrica primária e, se utilizada,
será reportada como análise exploratória.

## 7. Métricas textuais

Serão calculados de forma determinística:

- número de palavras;
- número de sentenças;
- média de palavras por sentença;
- proporção de palavras longas;
- diversidade lexical;
- número e profundidade de títulos;
- quantidade de listas e etapas;
- idioma predominante;
- índice de legibilidade validado para português.

A fórmula e a implementação do índice de legibilidade deverão ser citadas e verificadas
antes de congelar o código. Legibilidade não será interpretada automaticamente como
adequação pedagógica.

## 8. Métricas exploratórias de coerência

As seguintes medidas serão apresentadas como proxies, não como comprovação de qualidade:

- sobreposição entre conceitos do objetivo e metodologia/atividades;
- sobreposição entre conceitos do objetivo e estratégia de avaliação;
- uso dos materiais nas atividades;
- compatibilidade entre duração total e etapas temporizadas;
- presença de afirmações obrigatórias e proibidas cadastradas na tarefa.

Uma sobreposição lexical baixa não demonstra necessariamente incoerência semântica.
Consequentemente, essas métricas não compõem o desfecho primário.

## 9. Normalização textual

Antes da avaliação automática, o texto será:

- convertido para Unicode normalizado;
- comparado sem distinção entre maiúsculas e minúsculas;
- tokenizado preservando números e unidades;
- analisado com e sem diacríticos apenas para correspondência de termos;
- mantido integralmente no registro original.

Não serão removidas negações. Uma ocorrência dentro de contexto negado não contará como
atendimento positivo.

## 10. Respostas inválidas

Respostas vazias, recusas, idioma incorreto ou falhas técnicas recebem status de falha.
Elas não receberão artificialmente pontuação estrutural zero na análise primária. Serão
analisadas separadamente pela taxa de falha. Uma análise de sensibilidade poderá tratá-las
como zero, desde que explicitamente identificada.

## 11. Análise estatística

1. calcular métricas por repetição;
2. agregar as repetições por tarefa, condição e modelo;
3. usar a tarefa como bloco pareado;
4. comparar mais de duas condições pelo teste de Friedman;
5. realizar comparações pareadas pelo teste de Wilcoxon com correção de Holm;
6. reportar tamanho de efeito e intervalos de confiança;
7. analisar modelos e condições separadamente antes de qualquer agregação global.

O nível de significância e o método de intervalo de confiança deverão ser congelados no
manifesto antes das execuções.

## 12. Estudo de ablação

O estudo de ablação será secundário ao experimento C0–C1–C2. Partindo de C2, serão
criadas versões removendo individualmente:

- nível educacional;
- objetivo;
- duração;
- metodologia;
- materiais;
- estratégia de avaliação.

O tópico não será removido. As ablações não integrarão as 324 execuções do experimento
principal e terão planejamento amostral e manifesto próprios.

## 13. Limites das conclusões

As métricas permitem concluir sobre conformidade, completude, omissão, estabilidade e
desempenho computacional. Elas não permitem concluir, isoladamente, que:

- o conteúdo é pedagogicamente excelente;
- houve melhoria da aprendizagem;
- o professor economizou tempo;
- todas as afirmações são verdadeiras;
- o material pode ser usado sem revisão humana.

Todo material gerado deverá ser apresentado como rascunho sujeito à revisão docente.

## 14. LLM julgadora

Uma LLM julgadora será utilizada somente como métrica automática secundária para aspectos
semânticos que não podem ser medidos adequadamente por regras lexicais. A avaliação
principal continuará baseada nas métricas determinísticas desta rubrica.

A julgadora avaliará individualmente fidelidade semântica, alinhamento instrucional,
adequação declarada ao nível educacional e coerência/exequibilidade interna. Sua identidade,
versão, prompt, parâmetros, repetições e respostas brutas serão registrados. A julgadora
não receberá a condição experimental nem a identidade do modelo gerador.

O protocolo completo e a rubrica versionada estão em
`docs/LLM_AS_JUDGE_PROTOCOL.md` e `experiments/llm_judge_rubric.v1.json`. Antes do
experimento, a configuração deverá passar por testes metamórficos de anonimização,
duplicação, posição, verbosidade, omissão e desalinhamento controlados.

Não haverá avaliação humana, e as notas da LLM não serão descritas como verdade de
referência, validação docente ou comprovação de qualidade pedagógica.
