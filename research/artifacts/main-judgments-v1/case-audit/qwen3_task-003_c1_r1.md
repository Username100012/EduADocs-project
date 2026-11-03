001: **Plano de Aula: Uma Passagem de Trocas Adjacentes em Ordenação por Bolha**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação  
005: **Formação:** Introductory (Introdutória)  
006: **Objetivo de Aprendizagem:**  
007: - Simular uma passagem da esquerda para a direita de trocas adjacentes.  
008: - Explicar por que o maior valor termina na última posição após uma passagem completa.  
009: - Utilizar a resolução colaborativa de problemas como metodologia de ensino.  
010: - Registrar o vetor após cada comparação e justificar a posição final do maior valor como estratégia de avaliação.
011: 
012: ---
013: 
014: ### **I. Introdução (5 minutos)**
015: 
016: **Objetivo:** Estabelecer o contexto e o objetivo da aula.
017: 
018: - Apresentar o conceito de **ordenação por bolha** como uma técnica simples de ordenação de vetores.
019: - Explicar que a **passagem de trocas adjacentes** é a primeira etapa desse algoritmo.
020: - Introduzir a ideia de que, após uma passagem completa, o maior valor do vetor termina na última posição.
021: - Destacar que a aula será baseada em **resolução colaborativa de problemas**, com uso de **quadro e folha com sequências curtas de inteiros** como recursos.
022: 
023: ---
024: 
025: ### **II. Atividade 1: Introdução ao Algoritmo (10 minutos)**
026: 
027: **Metodologia:** Explicação direta com interação.
028: 
029: **Conteúdo:**
030: 
031: - Explicar o algoritmo de ordenação por bolha:
032:   - Comparar pares adjacentes de elementos.
033:   - Trocar os elementos se a ordem estiver invertida.
034:   - Repetir esse processo até que o vetor esteja ordenado.
035: - Apresentar o exemplo de passagem de trocas adjacentes com um vetor de 5 elementos.
036: - Mostrar o que acontece com o maior valor após uma passagem completa.
037: - Apresentar a **tarefa**:
038:   - Os alunos receberão um vetor de 5 inteiros aleatórios.
039:   - Eles devem simular uma passagem de trocas adjacentes, registrando o vetor após cada comparação.
040:   - O objetivo é identificar onde o maior valor termina após a passagem.
041: 
042: **Materiais:**
043: - Quadro para anotações.
044: - Folhas com sequências de inteiros (ex: [7, 3, 9, 1, 5]).
045: - Caneta, lápis, papel.
046: 
047: ---
048: 
049: ### **III. Atividade 2: Resolução Colaborativa (20 minutos)**
050: 
051: **Metodologia:** Trabalho em grupos de 2–3 alunos.
052: 
053: **Tarefa:**
054: - Cada grupo recebe um vetor de 5 inteiros (ex: [7, 3, 9, 1, 5]).
055: - Cada aluno deve simular a passagem de trocas adjacentes, registrando o vetor após cada comparação.
056: - O grupo deve discutir e justificar por que o maior valor termina na última posição após a passagem.
057: 
058: **Passos para simular a passagem:**
059: 1. Iniciar com o vetor inicial.
060: 2. Comparar o primeiro elemento com o segundo.
061: 3. Se a ordem estiver invertida, trocar os dois.
062: 4. Comparar o segundo elemento com o terceiro.
063: 5. Repetir até chegar ao penúltimo elemento.
064: 6. Após cada comparação, registrar o vetor no quadro.
065: 
066: **Exemplo de passagem:**
067: - Vetor inicial: [7, 3, 9, 1, 5]
068: - Passo 1: [3, 7, 9, 1, 5]
069: - Passo 2: [3, 7, 9, 1, 5] (não há troca)
070: - Passo 3: [3, 7, 1, 9, 5]
071: - Passo 4: [3, 7, 1, 5, 9]
072: - Final da passagem: [3, 7, 1, 5, 9]
073: 
074: **Justificativa:**
075: - O maior valor (9) termina na última posição após a passagem, pois ele só é movido para a direita quando o elemento à sua esquerda é maior que ele.
076: 
077: ---
078: 
079: ### **IV. Atividade 3: Discussão e Avaliação (10 minutos)**
080: 
081: **Metodologia:** Discussão coletiva com registros no quadro.
082: 
083: **Objetivo:**
084: - Avaliar a compreensão dos alunos sobre a passagem de trocas adjacentes.
085: - Verificar se os alunos conseguem identificar o padrão de movimento do maior valor.
086: 
087: **Avaliação:**
088: - Cada grupo apresenta o vetor após cada comparação.
089: - Discutir a justificativa do porquê o maior valor termina na última posição.
090: - Registrar as observações no quadro para análise coletiva.
091: 
092: **Perguntas para a discussão:**
093: - Por que o maior valor termina na última posição após uma passagem?
094: - Como o algoritmo se comporta em uma passagem completa?
095: - Qual é a vantagem de realizar múltiplas passagens?
096: 
097: ---
098: 
099: ### **V. Conclusão e Reforço (5 minutos)**
100: 
101: **Metodologia:** Resumo e encerramento.
102: 
103: **Conteúdo:**
104: - Resumir os principais pontos da aula:
105:   - A passagem de trocas adjacentes é a base da ordenação por bolha.
106:   - O maior valor termina na última posição após uma passagem.
107:   - O algoritmo é simples, mas pode ser lento para vetores grandes.
108: - Incentivar a prática com mais exemplos.
109: - Compartilhar a conclusão: **“O maior valor termina na última posição após uma passagem porque ele é movido para a direita em cada comparação, até que não haja mais elementos à sua esquerda.”**
110: 
111: ---
112: 
113: ### **VI. Recursos Utilizados:**
114: 
115: - **Quadro:** Para anotações e registros do vetor após cada passo.
116: - **Folhas com sequências de inteiros:** Para cada grupo.
117: - **Caneta, lápis, papel:** Para registro individual e coletivo.
118: - **Exemplo de vetor:** [7, 3, 9, 1, 5].
119: 
120: ---
121: 
122: ### **VII. Avaliação Formativa:**
123: 
124: - **Participação no grupo e discussão.**
125: - **Capacidade de simular a passagem de trocas adjacentes.**
126: - **Justificativa sobre o movimento do maior valor.**
127: 
128: ---
129: 
130: **Nota:** A aula pode ser adaptada para diferentes tamanhos de vetores (ex: 6 elementos) e para incluir uma segunda passagem, se aprofundando mais no algoritmo.
