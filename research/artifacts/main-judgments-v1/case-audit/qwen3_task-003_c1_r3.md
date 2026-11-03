001: **Plano de Aula: Uma Passagem de Trocas Adjacentes em Ordenação por Bolha**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação  
005: **Formação:** Introductory (Introdutória)  
006: **Objetivo de Aprendizagem:**  
007: - Simular uma passagem da esquerda para a direita de trocas adjacentes.  
008: - Explicar por que o maior valor termina na última posição após uma passagem completa.  
009: - Utilizar a **resolução colaborativa de problemas** como metodologia.  
010: - Registrar o vetor após cada comparação e justificar a posição final do maior valor como estratégia de avaliação.
011: 
012: ---
013: 
014: ## **1. Introdução (5 minutos)**
015: 
016: **Objetivo:** Introduzir o conceito de ordenação por bolha e a passagem de trocas adjacentes.
017: 
018: - **Pergunta inicial:**  
019:   *“Como você ordenaria uma lista de números de forma simples, repetindo passos até que a lista esteja em ordem?”*
020: 
021: - **Explicação breve sobre ordenação por bolha:**  
022:   - O algoritmo compara pares adjacentes de elementos e os troca se estiverem em ordem inversa.  
023:   - Cada passagem da esquerda para a direita do vetor resulta em um elemento maior "sobrar" na última posição.
024: 
025: - **Definição de passagem de trocas adjacentes:**  
026:   - Uma passagem completa do vetor, comparando cada par de elementos adjacentes e trocando-os se necessário.
027: 
028: ---
029: 
030: ## **2. Atividade Colaborativa: Simulação da Passagem (20 minutos)**
031: 
032: **Materiais:**  
033: - Quadro branco  
034: - Folhas com sequências curtas de inteiros (ex.: 5, 3, 8, 1, 2, 7)  
035: - Lápis e caneta
036: 
037: **Instruções para os alunos:**  
038: - Os alunos são divididos em grupos de 3 a 4 pessoas.  
039: - Cada grupo recebe uma sequência de inteiros.  
040: - Cada grupo deve simular uma passagem completa da esquerda para a direita, registrando o vetor após cada comparação.  
041: - Após cada comparação, o grupo deve justificar a troca ou não, explicando por que o valor foi ou não trocado.  
042: - Ao final da passagem, o grupo deve identificar o maior valor e justificar por que ele terminou na última posição.
043: 
044: **Exemplo de sequência:**
045: 
046: **Sequência inicial:** 5, 3, 8, 1, 2, 7  
047: 
048: **Passo 1:** Comparar 5 e 3 → troca → [3, 5, 8, 1, 2, 7]  
049: **Passo 2:** Comparar 5 e 8 → não troca → [3, 5, 8, 1, 2, 7]  
050: **Passo 3:** Comparar 8 e 1 → troca → [3, 5, 1, 8, 2, 7]  
051: **Passo 4:** Comparar 8 e 2 → troca → [3, 5, 1, 2, 8, 7]  
052: **Passo 5:** Comparar 8 e 7 → troca → [3, 5, 1, 2, 7, 8]  
053: 
054: **Resultado final:** [3, 5, 1, 2, 7, 8]  
055: **Maior valor:** 8 → está na última posição.
056: 
057: ---
058: 
059: ## **3. Discussão em Grupo (10 minutos)**
060: 
061: **Perguntas para discussão:**  
062: - O que acontece com o maior valor após uma passagem completa?  
063: - Por que o maior valor termina na última posição?  
064: - Como a passagem de trocas adjacentes contribui para a ordenação?  
065: - O que aconteceria se a passagem não terminasse com o maior valor na última posição?
066: 
067: **Registros:**  
068: - Cada grupo apresenta seus resultados e justificações.  
069: - O professor complementa com exemplos e explicações.  
070: - Os alunos discutem e compartilham suas estratégias de registro e justificativa.
071: 
072: ---
073: 
074: ## **4. Avaliação (5 minutos)**
075: 
076: **Critérios de Avaliação:**  
077: - Precisão na simulação da passagem de trocas adjacentes.  
078: - Justificativa clara sobre por que o maior valor termina na última posição.  
079: - Registro correto do vetor após cada comparação.  
080: - Participação ativa na discussão e colaboração em grupo.
081: 
082: **Forma de Avaliação:**  
083: - **Registros escritos** dos grupos.  
084: - **Explicação oral** de cada passo da simulação.  
085: - **Justificativa escrita** sobre a posição final do maior valor.
086: 
087: ---
088: 
089: ## **5. Conclusão e Refletir (5 minutos)**
090: 
091: **Conclusão:**  
092: - O algoritmo de ordenação por bolha é simples, mas eficiente apenas para listas pequenas.  
093: - Cada passagem da esquerda para a direita garante que o maior valor "sobrepõe" até a última posição.  
094: - A troca de elementos adjacentes é a base do algoritmo.
095: 
096: **Pergunta reflexiva:**  
097: - "Por que o algoritmo de bolha é considerado ineficiente para listas grandes?"
098: 
099: **Encerramento:**  
100: - Distribuição de exercícios para casa (opcional).  
101: - Comentário sobre o conteúdo e encerramento da aula.
102: 
103: ---
104: 
105: ## **Recursos Utilizados:**
106: 
107: - **Quadro branco** para anotações e registro de passos.  
108: - **Folhas com sequências de inteiros** para cada grupo.  
109: - **Lápis e caneta** para registro.  
110: - **Discussão em grupo** como estratégia de aprendizagem.  
111: - **Registros escritos** como estratégia de avaliação.
112: 
113: ---
114: 
115: **Notas Adicionais:**  
116: - A atividade pode ser adaptada para sequências de números maiores ou para diferentes tipos de dados (ex.: strings).  
117: - Pode-se incluir uma breve apresentação do algoritmo de bolha em pseudocódigo ou em linguagem de programação, se necessário.
