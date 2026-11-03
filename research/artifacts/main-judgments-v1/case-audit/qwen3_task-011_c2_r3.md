001: **PLANO DE AULA: Particionamento de Equivalência para Validação de Idade**
002: 
003: ---
004: 
005: ### **Tema:** Particionamento de equivalência para validação de idade  
006: **Nível educacional:** Graduação em Ciência da Computação – Formação introdutória  
007: **Duração:** 50 minutos  
008: **Metodologia:** Resolução colaborativa de problemas  
009: **Materiais e recursos:** Quadro, folha com a especificação de validação de idade inteira entre zero e 120  
010: **Estratégia de avaliação:** Entrega de classificação das partições e três entradas de teste com resultados esperados
011: 
012: ---
013: 
014: ## **1. Objetivo da aula:**
015: 
016: O aluno será capaz de:
017: - Identificar partições válidas e inválidas para um campo que aceita idades inteiras de zero a 120;
018: - Selecionar entradas de teste representativas que cobrem as classes de valores válidos e inválidos.
019: 
020: ---
021: 
022: ## **2. Conteúdo da aula:**
023: 
024: **Tópico:** Particionamento de equivalência (equivalence partitioning)  
025: **Subtópicos:**
026: - Conceito de equivalência em testes de software;
027: - Aplicação em validação de campos numéricos;
028: - Criação de partições para um campo de idade entre 0 e 120.
029: 
030: ---
031: 
032: ## **3. Estrutura da aula:**
033: 
034: ### **I. Introdução (5 minutos)**
035: 
036: **Objetivo:** Contextualizar o conceito de equivalência e sua aplicação na validação de dados.
037: 
038: **Atividade:**
039: - Apresentar o problema: "Você precisa validar um campo de entrada que aceita idades inteiras de 0 a 120."
040: - Explicar o conceito de equivalência: "Partições são conjuntos de valores que, ao serem testados, podem representar todas as possibilidades de entrada."
041: - Explicar o objetivo: "Através do particionamento, você identificará os valores que devem ser testados para garantir que o sistema funcione corretamente."
042: 
043: ---
044: 
045: ### **II. Explicação teórica (10 minutos)**
046: 
047: **Objetivo:** Introduzir os critérios para definir as partições.
048: 
049: **Conteúdo:**
050: - Definição de valores válidos e inválidos:
051:   - Valores válidos: 0 a 120 (inclusive).
052:   - Valores inválidos: menores que 0, maiores que 120.
053: - Exemplo de particionamento:
054:   - Valores válidos: [0, 120]
055:   - Valores inválidos: [-1, 121]
056: - Explicar a importância de testar os limites e valores representativos.
057: 
058: ---
059: 
060: ### **III. Atividade colaborativa (25 minutos)**
061: 
062: **Objetivo:** Classificar as entradas de teste em partições válidas e inválidas.
063: 
064: **Instruções:**
065: - O professor fornece uma lista de entradas de teste (exemplo: -5, 0, 10, 50, 120, 121, 1000, -100, 200, 0.5).
066: - Os alunos devem classificar cada entrada como "válida" ou "inválida".
067: - Cada grupo deve selecionar 3 entradas de teste que representem as classes de equivalência (valores válidos, valores inválidos, e possíveis bordas).
068: 
069: **Dica do professor:**
070: - "Lembre-se: o sistema aceita apenas valores inteiros entre 0 e 120."
071: 
072: **Resultado esperado:**
073: - Classificação das entradas;
074: - Seleção de 3 entradas de teste com resultados esperados (cobrindo classes válidas e inválidas).
075: 
076: ---
077: 
078: ### **IV. Discussão e apresentação (5 minutos)**
079: 
080: **Objetivo:** Discutir os resultados e validar a compreensão dos alunos.
081: 
082: **Atividade:**
083: - Cada grupo apresenta suas classificações e as entradas escolhidas.
084: - O professor corrige e complementa com exemplos.
085: - Reforça o conceito de equivalência e a importância de testar os limites.
086: 
087: ---
088: 
089: ### **V. Conclusão (5 minutos)**
090: 
091: **Objetivo:** Consolidar o aprendizado e motivar para a próxima aula.
092: 
093: **Resumo:**
094: - Particionamento de equivalência é uma técnica importante para testes de software.
095: - Em nosso caso, precisamos testar valores válidos e inválidos para garantir a validação correta de idades.
096: - O sistema aceita apenas valores inteiros entre 0 e 120.
097: 
098: **Encerramento:**
099: - "Na próxima aula, veremos como aplicar essa técnica em testes de entrada para outros campos."
100: 
101: ---
102: 
103: ## **4. Avaliação:**
104: 
105: - **Classificação das entradas de teste (valores válidos e inválidos):** 5 pontos
106: - **Seleção de 3 entradas de teste com resultados esperados (cobrindo classes válidas e inválidas):** 5 pontos
107: - **Participação na discussão e apresentação:** 5 pontos
108: 
109: **Total: 15 pontos**
110: 
111: ---
112: 
113: ## **5. Recursos utilizados:**
114: 
115: - Quadro
116: - Folha com especificação de validação de idade (exemplo de entradas de teste)
117: - Lápis, caneta e papel
118: 
119: ---
120: 
121: ## **6. Extensão (opcional):**
122: 
123: - Pode-se incluir um exemplo de código para validar o campo de idade (ex: Python, Java, etc.), para reforçar o conceito.
124: 
125: ---
126: 
127: **Fim do plano de aula.**
