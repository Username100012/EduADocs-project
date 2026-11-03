001: **Plano de Aula: Contagem de Números Pares em um Vetor**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação  
005: **Formação:** Introdutória  
006: **Objetivo de Aprendizagem:**  
007: Implementar em pseudocódigo a contagem de valores pares em um vetor e verificar os casos de vetor vazio e de vetor sem pares.  
008: **Metodologia:** Resolução colaborativa de problemas  
009: **Recursos:**  
010: - Quadro de giz  
011: - Folha com vetores contendo valores pares e ímpares  
012: - Papeis para anotações  
013: - Caneta e lápis  
014: - Computador com ambiente de desenvolvimento (opcional, para complementação)  
015: 
016: ---
017: 
018: ### **1. Introdução (5 minutos)**
019: 
020: **Objetivo:** Introduzir o conceito de vetor e a necessidade de contagem de elementos com propriedades específicas (como pares).
021: 
022: **Conteúdo:**
023: - Definição de vetor como estrutura de dados.
024: - Explicar o conceito de número par (divisível por 2).
025: - Apresentar o problema: contar os números pares em um vetor.
026: - Discutir os casos especiais: vetor vazio e vetor sem pares.
027: - Motivar a importância da lógica de controle (loops, condições) para resolver o problema.
028: 
029: **Atividade:**  
030: - Professor apresenta a definição de vetor e pares.  
031: - Pergunta: "Como você contaria os números pares em um vetor?"  
032: - Discutir possíveis abordagens (loop, condição, variável de contagem).
033: 
034: ---
035: 
036: ### **2. Resolução Colaborativa (25 minutos)**
037: 
038: **Objetivo:** Resolver o problema em grupo, utilizando o quadro e as folhas fornecidas.
039: 
040: **Passos:**
041: 
042: **a) Análise do Problema (5 minutos):**  
043: - Professor apresenta os dois casos testáveis:  
044:   - **Caso 1:** Vetor vazio  
045:   - **Caso 2:** Vetor sem pares  
046: - Alunos discutem como lidar com esses casos.
047: 
048: **b) Planejamento do Algoritmo (5 minutos):**  
049: - Alunos trabalham em grupos para planejar o algoritmo.  
050: - Professores orientam os grupos para que definam:  
051:   - Inicialização de variável de contagem.  
052:   - Loop sobre os elementos do vetor.  
053:   - Condição para verificar se o número é par.  
054:   - Atualização da variável de contagem.  
055:   - Tratamento do caso de vetor vazio.
056: 
057: **c) Implementação do Pseudocódigo (10 minutos):**  
058: - Cada grupo escreve o pseudocódigo no quadro com base em suas estratégias.  
059: - Professores ajudam a corrigir ou aprimorar as soluções.  
060: - Exemplo de pseudocódigo esperado:
061: 
062: ```
063: INICIO
064:     vetor = [1, 2, 3, 4, 5]
065:     cont_pares = 0
066:     PARA i DE 0 ATÉ TAMANHO(vetor) - 1
067:         SE vetor[i] % 2 == 0 ENTÃO
068:             cont_pares = cont_pares + 1
069:         FIM SE
070:     FIM PARA
071:     MOSTRAR cont_pares
072: FIM
073: ```
074: 
075: **d) Testes de Mesa (5 minutos):**  
076: - Alunos testam o pseudocódigo com os casos:  
077:   - Vetor vazio → resposta 0  
078:   - Vetor com todos ímpares → resposta 0  
079: - Alunos apresentam os resultados e justificam os casos.
080: 
081: ---
082: 
083: ### **3. Apresentação e Discussão (10 minutos)**
084: 
085: **Objetivo:** Revisar a solução, discutir os casos especiais e validar a lógica.
086: 
087: **Atividades:**
088: 
089: - Cada grupo apresenta o pseudocódigo e os testes de mesa.
090: - Professores validam a corretude e ressaltam a importância de lidar com os casos de vetor vazio e sem pares.
091: - Discussão sobre a importância da lógica de controle e da verificação de casos especiais.
092: - Professor apresenta uma versão final do pseudocódigo com comentários e explicação.
093: 
094: ---
095: 
096: ### **4. Avaliação (5 minutos)**
097: 
098: **Objetivo:** Avaliar o entendimento e a aplicação do conceito.
099: 
100: **Atividade:**
101: - Alunos recebem uma folha com um vetor aleatório e pedem que:
102:   - Escrevam o pseudocódigo para contar os pares.
103:   - Façam os testes de mesa com o vetor fornecido.
104:   - Justifiquem a estratégia usada.
105: 
106: ---
107: 
108: ### **5. Conclusão (5 minutos)**
109: 
110: **Objetivo:** Consolidar o aprendizado e planejar a próxima aula.
111: 
112: **Conteúdo:**
113: - Resumo do que foi aprendido: como contar pares em um vetor.
114: - Importância de testar casos especiais.
115: - Sugestão de próxima aula: algoritmos de ordenação ou busca em vetores.
116: - Agradecimento e encerramento.
117: 
118: ---
119: 
120: ### **Materiais Utilizados:**
121: 
122: - **Quadro e folha com vetores:** para atividades práticas.
123: - **Caneta e lápis:** para anotações.
124: - **Computador (opcional):** para apresentação de exemplos.
125: 
126: ---
127: 
128: ### **Justificativa da Estratégia:**
129: 
130: - A **resolução colaborativa** permite que os alunos explorem diferentes abordagens e aprendam com os erros e acertos dos colegas.
131: - O **uso de testes de mesa** ajuda a entender como o algoritmo funciona em diferentes cenários.
132: - A **verificação de casos especiais** (vetor vazio e sem pares) é essencial para desenvolver algoritmos robustos.
133: - O **pseudocódigo** é uma ferramenta intermediária que ajuda a entender a lógica antes de codificar em linguagem de programação.
134: 
135: ---
136: 
137: **Nota:** Este plano pode ser adaptado para incluir o uso de uma linguagem de programação específica, como Python ou Java, para reforçar o conceito.
