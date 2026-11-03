001: **Plano de Aula: Contagem de Números Pares em um Vetor**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação – Formação Introdutória  
005: **Objetivo de Aprendizagem:**  
006: - Implementar em pseudocódigo a contagem de valores pares em um vetor.  
007: - Verificar os casos de vetor vazio e de vetor sem pares.  
008: - Utilizar a metodologia de **resolução colaborativa de problemas**.  
009: - Utilizar **quadro e folha com vetores contendo valores pares e ímpares** como materiais e recursos.  
010: - **Produzir pseudocódigo e testes de mesa** para os casos mencionados.  
011: - **Justificar a contagem** como estratégia de avaliação.
012: 
013: ---
014: 
015: ### **1. Introdução (5 minutos)**
016: 
017: **Objetivo:** Introduzir o conceito de vetor e a necessidade de contar elementos com propriedades específicas (como pares).
018: 
019: **Conteúdo:**
020: 
021: - Definição de vetor: estrutura de dados que armazena uma coleção de elementos.
022: - Tipos de dados: inteiros, reais, etc.
023: - O que é um número par: divisível por 2.
024: - Motivação: para aplicar em algoritmos que precisam de análise de dados, como contagem de elementos, filtragem, etc.
025: 
026: **Atividade Inicial:**  
027: - Apresentar a definição de vetor e a propriedade de paridade (par/ímpar).  
028: - Perguntar: "Como você faria para contar quantos números pares existem em um vetor?"  
029: - Iniciar a discussão colaborativa com os alunos.
030: 
031: ---
032: 
033: ### **2. Resolução Colaborativa de Problemas (25 minutos)**
034: 
035: **Objetivo:** Guiar os alunos a desenvolver um pseudocódigo para contar números pares em um vetor, com base em exemplos fornecidos.
036: 
037: **Materiais:**
038: 
039: - **Quadro:** com exemplos de vetores (com valores pares, ímpares e vazio).
040: - **Folhas:** com os mesmos vetores para os alunos anotarem e testarem.
041: - **Pincel e papel:** para desenhar o pseudocódigo.
042: 
043: **Passo a passo:**
044: 
045: 1. **Dividir a turma em grupos de 3 a 4 alunos.**
046: 2. **Distribuir para cada grupo um vetor com valores (ex: [1, 2, 3, 4, 5, 6]).**
047: 3. **Iniciar a discussão:**
048:    - "Como você saberia se um número é par?"
049:    - "Como você faria para contar os pares em um vetor?"
050: 4. **Guia de discussão:**
051:    - Utilizar uma variável de contagem inicialmente zero.
052:    - Percorrer cada elemento do vetor.
053:    - Verificar se o elemento é par (usando `% 2 == 0`).
054:    - Se for par, incrementar a variável de contagem.
055:    - No final, imprimir o valor da variável de contagem.
056: 5. **Cada grupo deve produzir um pseudocódigo baseado nesse processo.**
057: 6. **Fazer testes de mesa para os seguintes casos:**
058:    - Vetor vazio: `[]`
059:    - Vetor com todos ímpares: `[1, 3, 5, 7]`
060:    - Vetor com alguns pares e ímpares: `[2, 4, 6, 1, 3, 5]`
061: 
062: **Perguntas para orientação:**
063: 
064: - "Como você trataria o caso de um vetor vazio?"
065: - "Como você saberia se não houver pares?"
066: - "Por que é importante testar todos os casos?"
067: 
068: ---
069: 
070: ### **3. Apresentação e Discussão (10 minutos)**
071: 
072: **Objetivo:** Apresentar os pseudocódigos e testes de mesa dos grupos, discutir resultados e identificar pontos de melhoria.
073: 
074: **Atividade:**
075: 
076: - Cada grupo apresenta seu pseudocódigo.
077: - Discutir os testes de mesa, destacando os casos de vetor vazio e sem pares.
078: - Comparar os pseudocódigos dos grupos.
079: - Identificar estratégias de contagem e validações.
080: 
081: **Perguntas para aula:**
082: 
083: - "Qual é a estratégia mais eficiente para contar pares?"
084: - "Por que é importante testar o caso de vetor vazio?"
085: - "Como você faria para validar a contagem de pares em um vetor?"
086: 
087: ---
088: 
089: ### **4. Conclusão e Avaliação (10 minutos)**
090: 
091: **Objetivo:** Revisar o conteúdo, reforçar a importância da resolução colaborativa e avaliar o aprendizado.
092: 
093: **Conteúdo:**
094: 
095: - Resumir o processo de contagem de pares em um vetor.
096: - Destacar a importância de testar todos os casos possíveis.
097: - Apresentar a estratégia de contagem como uma forma de avaliação prática.
098: - Enfatizar a importância de trabalhar em grupo e discutir soluções.
099: 
100: **Avaliação:**
101: 
102: - **Pseudocódigo produzido por cada grupo.**
103: - **Testes de mesa realizados para os casos de vetor vazio e sem pares.**
104: - **Participação na discussão e aplicação da metodologia de resolução colaborativa.**
105: 
106: ---
107: 
108: ### **5. Extensão (opcional – 5 minutos)**
109: 
110: **Objetivo:** Introduzir a possibilidade de aplicar esse algoritmo em linguagens de programação, como Python ou C.
111: 
112: **Conteúdo:**
113: 
114: - Exemplo de código em Python:
115:   ```python
116:   vetor = [2, 4, 6, 1, 3, 5]
117:   contador = 0
118:   for num in vetor:
119:       if num % 2 == 0:
120:           contador += 1
121:   print("Quantidade de pares:", contador)
122:   ```
123: 
124: - Incentivar a pensar em como esse código se aplicaria a outros problemas.
125: 
126: ---
127: 
128: ### **Recursos Utilizados:**
129: 
130: - **Quadro:** para apresentar exemplos.
131: - **Folhas:** para anotações e testes de mesa.
132: - **Pincel e papel:** para desenhar pseudocódigo.
133: 
134: ---
135: 
136: ### **Aprendizagem Esperada:**
137: 
138: - Os alunos deverão compreender como implementar um algoritmo de contagem de números pares em um vetor.
139: - Eles devem ser capazes de identificar e tratar os casos de vetor vazio e de vetor sem pares.
140: - Eles devem aplicar a metodologia de resolução colaborativa e produzir pseudocódigo com base em testes de mesa.
141: 
142: ---
143: 
144: **Fim do Plano de Aula** 🚀
