001: **Plano de Aula: Particionamento de Equivalência para Validação de Idade**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:**  
007: - Identificar partições válidas e inválidas para um campo que aceita idades inteiras de zero a 120.  
008: - Selecionar entradas de teste representativas para validar o comportamento do sistema.  
009: 
010: ---
011: 
012: ## **1. Introdução (5 minutos)**
013: 
014: **Objetivo:** Introduzir o conceito de *particionamento de equivalência* e sua aplicação na validação de dados.  
015: **Conteúdo:**  
016: - Definição de *particionamento de equivalência*: dividir o conjunto de valores possíveis em classes (ou partições) que são equivalentes para os propósitos de teste.  
017: - Exemplo: validar idades entre 0 e 120.  
018: - Importância da seleção de entradas de teste representativas para cobrir classes válidas e inválidas.  
019: 
020: **Materiais:**  
021: - Quadro branco  
022: - Folha com especificação de validação de idade inteira entre 0 e 120  
023: - Canetas e marcadores  
024: - Fichas de entrada de teste (opcional)  
025: 
026: ---
027: 
028: ## **2. Atividade de Particionamento (20 minutos)**
029: 
030: **Objetivo:** Dividir o intervalo de idades (0 a 120) em classes válidas e inválidas, com base em critérios lógicos.  
031: 
032: **Passos da Atividade:**  
033: 1. **Grupamento em Classes:**  
034:    - Compartilhar a folha com a especificação de validação.  
035:    - Discutir os limites do campo (0 a 120).  
036:    - Criar classes válidas e inválidas com base em valores extremos, valores normais e valores fora do intervalo.  
037: 
038: 2. **Identificar Partições:**  
039:    - **Partições válidas:**  
040:      - 0 a 120 (idade válida)  
041:      - 0 (idade zero)  
042:      - 120 (idade máxima)  
043:      - Valores normais, como 20, 40, 60, 80, 100.  
044:    - **Partições inválidas:**  
045:      - Menos de 0 (negativo)  
046:      - Maior que 120  
047:      - Não inteiros (ex: 25.5)  
048:      - Valores que não são números (ex: "trinta")  
049: 
050: 3. **Discussão em Grupo:**  
051:    - Os alunos discutem e classificam os valores em classes.  
052:    - Cada grupo apresenta suas partições e justificações.  
053:    - O professor fornece feedback e corrigi as falhas.  
054: 
055: **Resultado esperado:**  
056: - Os alunos identificam as partições válidas e inválidas de forma coletiva.  
057: - A folha é preenchida com as classes identificadas.  
058: 
059: ---
060: 
061: ## **3. Seleção de Entradas de Teste (15 minutos)**
062: 
063: **Objetivo:** Selecionar entradas de teste que representem as classes identificadas.  
064: 
065: **Passos da Atividade:**  
066: 1. **Revisar as Partições:**  
067:    - Os alunos revisam as classes válidas e inválidas identificadas.  
068: 
069: 2. **Seleção de Entradas:**  
070:    - **Entrada 1 (válida):** 20  
071:    - **Entrada 2 (válida):** 120  
072:    - **Entrada 3 (inválida):** -5  
073: 
074: 3. **Teste e Resultado Esperado:**  
075:    - Os alunos analisam as entradas e determinam se elas são válidas ou inválidas.  
076:    - O resultado esperado é informado no quadro.  
077: 
078: **Resultado esperado:**  
079: - Os alunos selecionam três entradas de teste que cobrem classes válidas e inválidas.  
080: - A folha é completada com as entradas de teste e resultados esperados.  
081: 
082: ---
083: 
084: ## **4. Avaliação e Conclusão (10 minutos)**
085: 
086: **Objetivo:** Avaliar o entendimento dos conceitos de partição e seleção de testes.  
087: 
088: **Atividade:**  
089: 1. **Classificação das Partições:**  
090:    - Os alunos classificam as partições válidas e inválidas identificadas.  
091:    - O professor verifica se as partições estão corretas.  
092: 
093: 2. **Seleção de Testes:**  
094:    - Os alunos explicam por que as entradas de teste escolhidas são representativas.  
095:    - O professor verifica se as entradas cobrem classes válidas e inválidas.  
096: 
097: 3. **Conclusão:**  
098:    - Resumir os conceitos de partição de equivalência.  
099:    - Destacar a importância da seleção de testes representativos.  
100:    - Encerrar a aula com uma pergunta de reflexão:  
101:      *"Por que é importante testar valores extremos e valores normais?"*  
102: 
103: ---
104: 
105: ## **5. Recursos Utilizados:**
106: - **Quadro e folha:** Para anotações e classificação.  
107: - **Fichas de entrada de teste (opcional):** Para auxiliar na atividade.  
108: - **Discussão em grupo:** Para a resolução colaborativa do problema.  
109: 
110: ---
111: 
112: ## **6. Estratégia de Avaliação:**
113: - **Classificação das Partições:** Verificar se os alunos identificaram as classes válidas e inválidas corretamente.  
114: - **Seleção de Entradas:** Verificar se os alunos selecionaram entradas que cobrem as classes identificadas.  
115: - **Participação em Discussão:** Avaliar a participação e a compreensão do grupo.  
116: 
117: ---
118: 
119: ## **7. Referências (opcional):**
120: - *Software Testing: A Craftsman's Approach* – Michael P. Krawitz  
121: - *Test-Driven Development: A Practical Guide* – Kent Beck  
122: - *Introduction to Software Testing* – Cemil D. Derman  
123: 
124: ---
125: 
126: **Nota:** Esta aula é adaptada para alunos que estão começando a trabalhar com testes de software, com ênfase em técnicas de partição de equivalência e seleção de testes. A abordagem colaborativa ajuda a consolidar conceitos teóricos em prática.
