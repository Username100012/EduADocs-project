001: **PLANO DE AULA – CONTAGEM DE NÚMEROS PARES EM UM VETOR**
002: 
003: **Tema:** Contagem de números pares em um vetor  
004: **Nível educacional:** Graduação em Ciência da Computação – Formação introdutória  
005: **Duração:** 50 minutos  
006: **Metodologia:** Resolução colaborativa de problemas  
007: **Materiais e recursos:** Quadro, folha com vetores contendo valores pares e ímpares, lápis, caneta, papel, projetor (opcional)  
008: **Estratégia de avaliação:** Produzir pseudocódigo e testes de mesa para casos de vetor vazio e vetor sem pares, justificando a contagem
009: 
010: ---
011: 
012: ### **1. INTRODUÇÃO (5 minutos)**
013: 
014: **Objetivo:** Estabelecer o contexto da aula e motivar os alunos para a atividade.
015: 
016: - Apresentar o conceito de **vetor** e **números pares**.
017: - Explicar o objetivo da aula: **contar quantos números pares existem em um vetor**.
018: - Destacar a importância de tratar casos especiais como **vetor vazio** e **vetor sem pares**.
019: - Apresentar a **metodologia de resolução colaborativa**, incentivando a participação e o trabalho em grupo.
020: 
021: ---
022: 
023: ### **2. AULA PRÁTICA (35 minutos)**
024: 
025: **Aula dividida em etapas:**
026: 
027: #### **Etapa 1: Revisão de conceitos (5 minutos)**
028: 
029: - Revisar os conceitos de:
030:   - **Vetor**: estrutura de dados que armazena uma coleção de elementos.
031:   - **Números pares**: números divisíveis por 2 (ex.: 2, 4, 6).
032:   - **Testes de mesa**: ferramenta para validar algoritmos passo a passo.
033: 
034: #### **Etapa 2: Introdução ao pseudocódigo (10 minutos)**
035: 
036: - Apresentar um exemplo de pseudocódigo para a contagem de pares em um vetor.
037: - Incentivar os alunos a analisar o pseudocódigo e identificar os passos principais.
038: - Destacar a necessidade de **tratamento de erros** e **casos especiais**.
039: 
040: **Exemplo de pseudocódigo (modelo):**
041: 
042: ```
043: INICIO
044:     DECLARAR vetor COM 5 ELEMENTOS
045:     CONTADOR = 0
046:     PARA i DE 0 ATÉ 4 FAZ
047:         SE vetor[i] % 2 == 0 ENTAO
048:             CONTADOR = CONTADOR + 1
049:         FIM SE
050:     FIM PARA
051:     IMPRIMIR CONTADOR
052: FIM
053: ```
054: 
055: #### **Etapa 3: Trabalho em grupo (20 minutos)**
056: 
057: - Dividir os alunos em grupos de 3 a 4 pessoas.
058: - Distribuir para cada grupo um **vetor de números** (com valores pares e ímpares).
059: - Cada grupo deve:
060:   1. Escrever o pseudocódigo para contar os números pares.
061:   2. Fazer **testes de mesa** para:
062:      - Vetor vazio
063:      - Vetor com apenas números ímpares
064:      - Vetor com alguns pares e alguns ímpares
065:   3. Justificar os resultados obtidos.
066:   4. Apresentar os resultados ao grupo.
067: 
068: #### **Etapa 4: Apresentação e discussão (5 minutos)**
069: 
070: - Cada grupo apresenta seu pseudocódigo e resultados dos testes.
071: - Discutir os casos especiais:
072:   - O que acontece se o vetor estiver vazio?
073:   - O que acontece se o vetor não tiver pares?
074: - Reforçar a importância de testar todos os casos.
075: 
076: ---
077: 
078: ### **3. CONCLUSÃO E REFLEXÃO (5 minutos)**
079: 
080: - Resumir os principais pontos da aula.
081: - Destacar a importância de:
082:   - Trabalhar com **casos especiais** em algoritmos.
083:   - Fazer **testes de mesa** para validar a lógica.
084:   - Compartilhar conhecimentos em grupo.
085: - Atribuir uma tarefa opcional para os alunos: escrever um programa em Python que realize a mesma funcionalidade.
086: 
087: ---
088: 
089: ### **4. AVAIAÇÃO**
090: 
091: - **Produção de pseudocódigo** com estrutura correta e lógica clara.
092: - **Testes de mesa** com casos de vetor vazio e sem pares, com justificativa.
093: - **Participação ativa** no trabalho em grupo e na discussão.
094: - **Entrega de pseudocódigo e testes de mesa** para cada grupo.
095: 
096: ---
097: 
098: ### **5. EXTENSÃO (opcional)**
099: 
100: - Para alunos com maior nível, sugerir a implementação em linguagem de programação (Python, C, Java).
101: - Incentivar a criação de uma função genérica para contar pares em qualquer vetor.
102: 
103: ---
104: 
105: **Fim do plano de aula.**
