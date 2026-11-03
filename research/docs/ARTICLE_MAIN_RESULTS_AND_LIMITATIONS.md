# Resultados e limitações — estudo computacional principal

Rascunho para revisão dos autores, preparado em 27/10/2026 exclusivamente com os dados principais já coletados. Os resultados do piloto e dos diagnósticos não são somados a este conjunto. Numeração de seções e tabelas deverá ser ajustada ao manuscrito. Nenhuma nova chamada às APIs foi realizada nesta integração.

## Resultados

### Composição do conjunto analisado

A coleta principal compreendeu 12 tarefas introdutórias de Ciência da Computação, distribuídas entre Algoritmos e Programação, Banco de Dados e Engenharia de Software. Para cada tarefa, foram previstas três gerações em cada uma das condições C0, C1 e C2, com dois geradores: Gemini (`gemini-3.8-flash`) e Qwen3 4B quantizado em Q4_K_M, executado via Ollama. Das 216 tentativas previstas, 215 produziram textos: 107 no Gemini e 108 no Qwen3. Uma chamada Gemini em C1, referente à tarefa 002, terminou em timeout e permaneceu registrada sem texto. Todas as respostas disponíveis apresentaram motivo de término normal reportado pelo fornecedor; isso não certifica completude ou correção do conteúdo.

Os 215 planos originaram 645 tentativas de julgamento com GPT (`gpt-6.1-sol`), três por plano. Foram obtidos 624 julgamentos válidos; 15 respostas foram rejeitadas por divergência literal das citações em relação ao texto de origem e seis chamadas falharam por falta de crédito. A execução foi retomada apenas para identificadores ainda não enviados, preservando os erros anteriores. Nenhum julgamento foi reparado ou repetido. As notas secundárias utilizaram 196 planos com três julgamentos válidos; os 19 planos com trincas incompletas não receberam nota zero. Os julgamentos válidos desses planos foram mantidos nas frequências nominais dos requisitos.

As 624 respostas válidas foram novamente processadas pelo validador local, reproduzindo os registros salvos, e as 15 rejeições foram reproduzidas. Essa verificação estabelece consistência do processamento e correspondência literal das citações, sem comprovar correção dos julgamentos.

### Notas secundárias e indicadores operacionais

A Tabela 1 apresenta as notas de alinhamento instrucional e coerência textual, estimadas pela julgadora em escala ordinal autoral de 1 a 4, juntamente com os indicadores de geração. Para as notas, calculou-se a mediana de três julgamentos válidos por plano, seguida da mediana dos planos por tarefa e da mediana entre as 12 tarefas. Para latência e tokens, calcularam-se medianas por tarefa e, posteriormente, a mediana entre tarefas. Dessa forma, as tarefas receberam pesos iguais; julgamentos e gerações repetidos não foram tratados como unidades experimentais independentes.

**Tabela 1. Notas secundárias e indicadores de geração por modelo e condição.**

| Gerador | Condição | Planos | Trincas válidas | Alinhamento | Coerência | Latência (s) | IQR¹ (s) | Tokens de entrada | Tokens de saída |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini | C0 | 36 | 31 | 3 | 4 | 18.08 | 2.13 | 23 | 1568.5 |
| gemini | C1 | 35 | 32 | 4 | 4 | 15.96 | 2.62 | 135.5 | 1335.5 |
| gemini | C2 | 36 | 33 | 4 | 4 | 14.89 | 1.98 | 189.5 | 1149 |
| qwen3 | C0 | 36 | 33 | 3 | 3 | 23.02 | 3.75 | 40 | 1146 |
| qwen3 | C1 | 36 | 33 | 4 | 3 | 28.19 | 3.05 | 177 | 1360 |
| qwen3 | C2 | 36 | 34 | 4 | 3 | 23.38 | 3.44 | 235 | 1133.5 |

¹ IQR entre as 12 medianas de latência por tarefa, não entre todas as chamadas. Tokens são contagens reportadas pelos respectivos fornecedores; as medianas podem ser fracionárias e não são diretamente comparáveis entre tokenizadores. O timeout está excluído dos indicadores sem dados disponíveis, sem imputação de zero.

Nos dois geradores, C1 e C2 apresentaram mediana de alinhamento igual a 4. A coerência teve mediana 4 no Gemini e 3 no Qwen3, sem diferença entre C1 e C2. Em C0, o alinhamento teve mediana 3 nos dois modelos. Essa diferença deve ser interpretada considerando que C0 recebeu somente o tipo de material e o tópico, enquanto C1 e C2 receberam os sete requisitos. Assim, C0/C1 altera a informação disponível; o contraste C1/C2 mantém o conteúdo informacional e modifica sua organização. O empate das medianas entre C1 e C2 não demonstra equivalência e pode ocultar diferenças entre tarefas e concentração no limite superior da escala.

Na configuração observada, C2 apresentou medianas menores de latência e tokens de saída do que C1 nos dois geradores, apesar da maior quantidade de tokens de entrada. No Gemini, as medianas de latência foram 15,96 s em C1 e 14,89 s em C2; no Qwen3, 28,19 s e 23,38 s. As medianas de saída foram, respectivamente, 1.335,5 e 1.149 tokens no Gemini, e 1.360 e 1.133,5 no Qwen3. Esses resultados descrevem a execução estudada e não isolam o efeito causal da estrutura: o tamanho das respostas, os parâmetros, o ambiente de execução e, no serviço remoto, a rede e a carga também podem afetar os tempos.

A dispersão inclui ocorrências que as medianas não representam integralmente. A maior latência registrada em uma resposta Gemini C0 foi 1.679,07 s, enquanto os máximos em C1 e C2 foram 186,77 s e 184,12 s. Esses registros foram preservados, sem exclusão posterior por serem extremos; sua causa não foi estabelecida. No Qwen3, os máximos variaram de 30,95 s a 33,80 s. A comparação entre serviço remoto e execução local não constitui benchmark controlado de hardware ou desempenho intrínseco dos modelos.

### Classificação dos sete requisitos

Os requisitos foram mantidos como cinco categorias nominais: supported, partial, not_addressed, contradicted e uncertain. A Tabela 2 apresenta a frequência de supported em C1 e C2, com o total de julgamentos válidos de cada célula. Esses percentuais descrevem decisões da julgadora, sem constituir taxa de acurácia, proporção de planos independentes ou nota global. As distribuições completas das cinco categorias e os recortes por tarefa permanecem nos artefatos de análise.

**Tabela 2. Julgamentos classificados como supported no contraste C1/C2.**

| Requisito | Gemini C1 | Gemini C2 | Qwen3 C1 | Qwen3 C2 |
|---|---:|---:|---:|---:|
| Tópico | 101/101 (100.0%) | 105/105 (100.0%) | 105/105 (100.0%) | 106/106 (100.0%) |
| Nível escolar | 101/101 (100.0%) | 105/105 (100.0%) | 105/105 (100.0%) | 106/106 (100.0%) |
| Objetivos | 101/101 (100.0%) | 105/105 (100.0%) | 99/105 (94.3%) | 96/106 (90.6%) |
| Duração | 101/101 (100.0%) | 105/105 (100.0%) | 77/105 (73.3%) | 68/106 (64.2%) |
| Metodologia | 101/101 (100.0%) | 105/105 (100.0%) | 105/105 (100.0%) | 106/106 (100.0%) |
| Materiais | 97/101 (96.0%) | 105/105 (100.0%) | 78/105 (74.3%) | 106/106 (100.0%) |
| Estratégia de avaliação | 101/101 (100.0%) | 105/105 (100.0%) | 95/105 (90.5%) | 101/106 (95.3%) |

No Gemini, seis requisitos receberam supported em todos os julgamentos válidos de C1 e C2; materiais passou de 97/101 para 105/105. No Qwen3, tópico, nível escolar e metodologia também ficaram no limite superior nas duas condições. Materiais apresentou maior frequência de supported em C2, assim como a estratégia de avaliação. Em contrapartida, objetivos e duração apresentaram menor frequência nessa categoria. Esses resultados não permitem concluir superioridade geral da instrução estruturada.

As demais categorias ajudam a interpretar as diferenças. Nos objetivos do Qwen3, C1 apresentou seis contradicted, enquanto C2 apresentou nove partial e um contradicted. Na duração, C1 apresentou 28 contradicted; C2 apresentou 21 contradicted e 17 uncertain. Portanto, uma redução em supported não implica, necessariamente, aumento de contradições. As frequências agrupadas têm denominadores afetados pelas falhas e não substituem a comparação por tarefa.

A análise por tarefa mostrou direções distintas. Nos objetivos de GROUP BY/COUNT, o Qwen3 passou de 9/9 supported em C1 para 0/9 em C2, com nove partial. Em rastreabilidade, passou de 2/8 supported em C1 para 8/9 em C2. Na duração, a frequência de supported aumentou em cinco tarefas, diminuiu em cinco e permaneceu em 100% em duas. O resultado agregado não caracteriza melhoria uniforme.

### Análise complementar de sensibilidade aos dados ausentes

Após a análise principal, foi realizado um recorte de casos completos pareados por gerador, tarefa e número de repetição da geração. Cada par foi incluído somente quando C1 e C2 apresentaram, ambos, três julgamentos válidos. Permaneceram 30 dos 36 pares previstos no Gemini e 31 dos 36 no Qwen3, com as 12 tarefas representadas em ambos. Os denominadores passaram a ser iguais entre condições: 90 julgamentos válidos por condição no Gemini e 93 no Qwen3. O pareamento é administrativo; não implica independência das repetições ou compartilhamento de sorteios entre condições.

As medianas secundárias permaneceram inalteradas. No Qwen3, as frequências de supported continuaram maiores em C2 para materiais (100% versus 72,0%) e estratégia de avaliação (94,6% versus 89,2%), e menores para objetivos (89,2% versus 93,5%) e duração (61,3% versus 76,3%). No Gemini, materiais passou de 95,6% em C1 para 100% em C2, enquanto os demais requisitos permaneceram em 100%. Assim, o recorte não inverteu as direções dos contrastes agrupados observados. Essa análise pós-coleta sustenta a manutenção da interpretação descritiva sob esta regra de seleção, mas não demonstra ausência de viés dos dados ausentes, equivalência entre condições ou correção da julgadora. As frequências agrupadas continuam refletindo números diferentes de pares entre tarefas e não substituem as notas com peso igual por tarefa.

### Auditoria exploratória e limites dos instrumentos

A auditoria computacional pós-coleta reuniu os 72 planos Qwen3 de C1/C2 para inspeção dos cronogramas e os 12 planos das tarefas GROUP BY/COUNT e rastreabilidade para investigação dos objetivos. Sua seleção foi motivada pelos resultados já observados e não constitui uma amostra independente para estimar acurácia da julgadora. As classificações originais foram preservadas.

Foram identificadas inconsistências verificáveis nos materiais. Em dois planos de GROUP BY/COUNT de C2, as etapas somaram 55 minutos, apesar da duração declarada de 50. Em um plano de INNER JOIN de C2, os intervalos da tabela totalizaram 50 minutos, mas duas linhas apresentaram rótulos de duração incompatíveis com os próprios intervalos. Assim, a declaração do tempo total, isoladamente, não demonstra consistência do cronograma.

Também foi identificado um erro aritmético da julgadora. Em um plano de INNER JOIN de C1, as etapas de 5, 25, 10, 5 e 5 minutos totalizam 50, mas um julgamento afirmou que totalizavam 55 e atribuiu contradicted. Os outros dois julgamentos calcularam 50 e atribuíram supported. O exemplo evidencia que citações autênticas podem acompanhar uma justificativa incorreta; não permite calcular uma taxa geral de erro a partir da auditoria selecionada.

Nos objetivos, uma classificação partial em GROUP BY/COUNT decorreu da falta de explicitação de que a tabela seria pequena, embora o texto contemplasse a consulta e a comparação do resultado. Em rastreabilidade, um exemplo marcava todos os requisitos como cobertos na matriz e simultaneamente afirmava que um deles não tinha teste. Dois julgamentos mantiveram supported para objetivos por considerar sua declaração explícita, enquanto um atribuiu contradicted por considerar a inconsistência do exemplo. Os três atribuíram alinhamento 2 e coerência 1. Esse caso demonstra variação na fronteira entre representação do objetivo e realização consistente da atividade, sem indicar que a julgadora tenha ignorado o defeito em todos os critérios.

O observador sintático apresentou limites distintos. Foram preservados 79 estados empty, que indicam ausência de conteúdo associado pelo parser ao rótulo reconhecido, não seções necessariamente vazias. O extrator temporal congelado reconhece declarações e intervalos previstos, mas não soma títulos arbitrários de etapas. Por exemplo, embora os 36 planos Qwen3 C2 apresentassem declaração temporal igual ao alvo segundo esse extrator, a auditoria encontrou cronogramas internamente inconsistentes. Os instrumentos medem aspectos diferentes e não devem ser apresentados como validação recíproca.

### Consumo e estimativa de custo

As 107 respostas Gemini com consumo disponível corresponderam a uma estimativa bruta de US$ 0,554391, calculada com os preços de referência congelados no protocolo. A saída faturável foi inferida pela diferença entre tokens totais e tokens de entrada, incluindo raciocínio uma única vez. A estimativa não é uma fatura, não presume descontos de cache e não inclui eventual custo desconhecido do timeout. Não foram medidos consumo energético, custo de hardware ou custo total da execução local.

Nos julgamentos GPT, 639 tentativas apresentaram dados de uso: as 624 respostas válidas e as 15 rejeitadas pela validação. Foram reportados 2.305.277 tokens de entrada e 1.377.030 de saída, totalizando 3.682.307 tokens. As seis chamadas rejeitadas por crédito não apresentaram consumo reportado. Respostas inválidas podem consumir tokens; sua exclusão analítica não elimina o consumo operacional. Esses totais descrevem somente o lote principal de julgamento e não incluem o piloto, os diagnósticos ou testes de acesso. Não foi inferida uma fatura OpenAI a partir desses totais, pois o faturamento depende também do tratamento de cache.

## Limitações e ameaças à validade

O estudo é restrito à geração de planos de aula em português para 12 tarefas introdutórias de Computação. O mapeamento ao referencial da SBC orienta a seleção, mas não demonstra representatividade curricular, equivalência de dificuldade ou generalização para outras áreas, níveis de ensino, idiomas e tipos de material do EduADocs. Não foram avaliados ganhos de aprendizagem, usabilidade ou eficácia pedagógica.

As estimativas semânticas dependem de uma única família de julgadora e de uma configuração fixa. As três repetições permitem observar estabilidade, mas não são avaliações independentes de especialistas e podem compartilhar erros. A auditoria demonstrou um erro aritmético e diferenças na aplicação das categorias, reforçando que conformidade do JSON e correspondência literal das citações não asseguram validade da decisão. A concentração de classificações e notas no limite superior também reduz a discriminação observada entre condições.

A mensuração automática de campos depende de rótulos, hierarquia e padrões reconhecidos. Campos não detectados e estados empty não comprovam omissão semântica; a concordância de uma duração declarada com o alvo não comprova consistência de todas as etapas. A análise exploratória adicional foi mantida separada, sem recalibrar os instrumentos ou recodificar os resultados principais após observar as respostas.

O desenho compara apenas duas configurações de geradores, com parâmetros e ambientes diferentes. No Qwen3, a seed fixa e a ocorrência de textos idênticos limitam a independência das repetições: foram observados 29, 29 e 24 textos distintos em C0, C1 e C2, entre 36 respostas por condição. No Gemini, os 36, 35 e 36 textos disponíveis foram distintos dentro de cada condição. Não se atribui às diferenças de tempo ou consumo um efeito isolado da família, do tamanho do modelo, da execução local ou da organização do prompt. Identificadores hospedados não são garantia de snapshots imutáveis.

As falhas de geração e julgamento produziram denominadores diferentes entre células e trincas incompletas. Sua preservação evita repetição seletiva e imputação artificial de zero, mas não garante que os dados ausentes sejam aleatórios ou que as comparações estejam livres de viés de seleção. As notas usam somente trincas completas; as frequências nominais usam todos os julgamentos válidos e incluem repetições dependentes. A análise é descritiva, sem teste de significância, escore composto ou teste de equivalência.

Finalmente, C0 omite seis requisitos apresentados em C1/C2. Seu contraste com as demais condições não isola o efeito da estrutura nem constitui ablação individual de requisitos. Os resultados de C1/C2 mostram diferenças localizadas, sem sustentar superioridade geral de C2. Não houve revisão cega por especialistas, avaliação com docentes ou estudantes, verificação sistemática da correção factual e algorítmica, segurança ou viés. Os achados devem ser interpretados como avaliação computacional das configurações estudadas, sem alegar validação pedagógica.

## Rastreabilidade para revisão dos autores

- [Protocolo congelado](MAIN_STUDY_PROTOCOL.md).
- [Indicadores automáticos](../artifacts/main-study-v1/AUTOMATIC_METRICS.md).
- [Tabelas nominais e notas](../artifacts/main-judgments-v1/RESULTS.md).
- [Comparação dos requisitos por tarefa](../artifacts/main-judgments-v1/REQUIREMENTS_COMPARISON.md).
- [Auditoria exploratória com casos e evidências](../artifacts/main-judgments-v1/case-audit/AUDIT.md).
- [Revalidação dos julgamentos](../artifacts/main-judgments-v1/consolidation_audit.json).
- [Tabela integrada em CSV](../artifacts/main-judgments-v1/integrated_results.csv).

Este rascunho reporta os achados empíricos. As referências científicas e os detalhes completos do método devem permanecer nas seções correspondentes do manuscrito; não se transfere a validação de benchmarks publicados às métricas autorais deste estudo.
