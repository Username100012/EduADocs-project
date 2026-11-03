001: **Plano de Aula: Particionamento de Equivalência para Validação de Idade**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:**  
007: Identificar partições válidas e inválidas para um campo que aceita idades inteiras de zero a 120 e selecionar entradas de teste representativas.
008: 
009: ---
010: 
011: ## **1. Introdução (5 minutos)**
012: 
013: **Objetivo:** Introduzir o conceito de particionamento de equivalência e sua aplicação na validação de campos de entrada.
014: 
015: **Conteúdo:**
016: - Definição de particionamento de equivalência.
017: - Aplicação em testes de software: identificar valores que pertencem a classes válidas ou inválidas.
018: - Exemplo: validação de campo de idade (0 a 120).
019: 
020: **Atividade Inicial:**
021: - O professor apresenta a especificação do campo de idade: "Aceita idades inteiras de 0 a 120".
022: - Pergunta: "Qual é a faixa de valores válidos para este campo?"
023: - Resposta esperada: "Valores de 0 a 120, inclusive."
024: 
025: ---
026: 
027: ## **2. Particionamento de Equivalência (15 minutos)**
028: 
029: **Objetivo:** Ensinar como dividir os valores em classes válidas e inválidas, com base na especificação.
030: 
031: **Materiais:**
032: - **Quadro:** com a especificação do campo de idade.
033: - **Folha:** com a tabela de particionamento.
034: 
035: **Atividade:**
036: - O professor divide a turma em grupos de 3 a 4 alunos.
037: - Cada grupo recebe a especificação do campo de idade e uma folha com uma tabela de particionamento.
038: - Cada grupo deve identificar as classes válidas e inválidas para o campo de idade.
039: - Exemplo de classes:
040:   - Válido: 0 a 120
041:   - Inválido: <0 ou >120
042: 
043: **Discussão:**
044: - O professor pede que cada grupo apresente suas classes.
045: - Revisão coletiva: identificar as classes válidas e inválidas.
046: - O professor corrige e complementa as respostas.
047: 
048: ---
049: 
050: ## **3. Seleção de Entradas de Teste (15 minutos)**
051: 
052: **Objetivo:** Selecionar entradas de teste representativas para cobrir as classes identificadas.
053: 
054: **Atividade:**
055: - Cada grupo recebe uma lista de valores (ex: -5, 0, 10, 50, 120, 121, 200).
056: - Cada grupo deve classificar cada valor como válido ou inválido, com base nas classes identificadas.
057: - O professor pede que cada grupo selecione 3 entradas de teste, cobrindo classes válidas e inválidas.
058: 
059: **Exemplo de entrada de teste:**
060: - Válido: 0
061: - Válido: 50
062: - Inválido: 121
063: 
064: **Discussão:**
065: - O professor pede que os grupos apresentem suas escolhas.
066: - Revisão coletiva: validar se as entradas cobrem as classes válidas e inválidas.
067: - O professor fornece as classificações corretas.
068: 
069: ---
070: 
071: ## **4. Avaliação (5 minutos)**
072: 
073: **Objetivo:** Avaliar a capacidade dos alunos de identificar classes válidas e inválidas e selecionar entradas de teste.
074: 
075: **Avaliação:**
076: - Classificação das classes: válidas e inválidas.
077: - Seleção de entradas de teste: cobrindo classes válidas e inválidas.
078: 
079: **Resultado Esperado:**
080: - Os alunos devem identificar as classes válidas (0 a 120) e inválidas (<0 ou >120).
081: - Deverão selecionar entradas de teste que representem essas classes.
082: 
083: ---
084: 
085: ## **5. Conclusão e Perguntas Finais (5 minutos)**
086: 
087: **Conclusão:**
088: - Resumo do processo de particionamento de equivalência.
089: - Importância da seleção de entradas de teste para testes de validação.
090: 
091: **Perguntas Finais:**
092: 1. Como você identificaria as classes válidas e inválidas para um campo de data?
093: 2. Por que é importante cobrir classes válidas e inválidas em testes?
094: 3. Como a metodologia de particionamento de equivalência ajuda no planejamento de testes?
095: 
096: ---
097: 
098: ## **Materiais e Recursos:**
099: - **Quadro:** com a especificação do campo de idade.
100: - **Folha:** com a tabela de particionamento e valores de teste.
101: - **Caneta, lápis, papel.**
102: 
103: ---
104: 
105: ## **Avaliação:**
106: - **Classe válida:** 0 a 120 (inclusivo).
107: - **Classe inválida:** <0 ou >120.
108: 
109: ---
110: 
111: ## **Entradas de Teste Selecionadas:**
112: 1. **Válido:** 0  
113: 2. **Válido:** 50  
114: 3. **Inválido:** 121
115: 
116: ---
117: 
118: **Nota:** Este plano de aula está alinhado com os princípios de testes de software, incluindo **testes de equivalência** e **testes de limites**, e é adequado para alunos iniciantes em ciência da computação.
