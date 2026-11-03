001: **Plano de Aula: Uma Passagem de Trocas Adjacentes em Ordenação por Bolha**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação  
005: **Formação:** Introductory (Introdutória)  
006: **Metodologia:** Resolução colaborativa de problemas  
007: **Recursos:** Quadro, folha com sequências curtas de inteiros, canetas, marcadores, lápis, papel quadriculado
008: 
009: ---
010: 
011: ### **Objetivo de Aprendizagem:**
012: Simular uma passagem da esquerda para a direita de trocas adjacentes e explicar por que o maior valor termina na última posição após a passagem completa.
013: 
014: ---
015: 
016: ## **I. Introdução (5 minutos)**
017: 
018: - **Objetivo:** Introduzir o conceito de ordenação por bolha e destacar a importância da passagem de trocas adjacentes.
019: - **Conteúdo:**
020:   - Definir ordenação por bolha como um algoritmo simples de ordenação.
021:   - Explicar que a passagem de trocas adjacentes é a etapa em que os elementos são comparados dois a dois e trocados se estiverem em ordem inversa.
022:   - Destacar que, após uma passagem completa, o maior valor termina na última posição, pois é "empurrado" para a direita com cada comparação.
023: 
024: - **Apoio visual:** Desenhar no quadro a estrutura do algoritmo e a ideia de "bolhas" que se movem para a direita.
025: 
026: ---
027: 
028: ## **II. Atividade de Resolução Colaborativa (30 minutos)**
029: 
030: ### **Passo 1: Distribuição de materiais (2 minutos)**
031: 
032: - Distribuir para cada grupo de 3–4 alunos:
033:   - Uma folha com uma sequência de 5 a 7 números inteiros aleatórios (ex: 7, 2, 5, 3, 9, 1, 4).
034:   - Canetas, lápis, papel quadriculado para registrar as mudanças.
035: 
036: ### **Passo 2: Simulação da passagem de trocas adjacentes (25 minutos)**
037: 
038: - **Instruções:**
039:   - Os alunos devem simular uma passagem da esquerda para a direita, comparando pares consecutivos e trocando os elementos se estiverem em ordem inversa.
040:   - Após cada comparação, devem **registrar o vetor** no papel quadriculado.
041:   - O objetivo é **identificar o maior valor** e ver como ele "se move" para a direita.
042: 
043: **Exemplo de sequência:**
044: **[7, 2, 5, 3, 9, 1, 4]**
045: 
046: **Passo a passo:**
047: 
048: 1. Comparar 7 e 2 → 7 > 2 → trocar → [2, 7, 5, 3, 9, 1, 4]
049: 2. Comparar 7 e 5 → 7 > 5 → trocar → [2, 5, 7, 3, 9, 1, 4]
050: 3. Comparar 7 e 3 → 7 > 3 → trocar → [2, 5, 3, 7, 9, 1, 4]
051: 4. Comparar 7 e 9 → 7 < 9 → não trocar → [2, 5, 3, 7, 9, 1, 4]
052: 5. Comparar 9 e 1 → 9 > 1 → trocar → [2, 5, 3, 7, 1, 9, 4]
053: 6. Comparar 9 e 4 → 9 > 4 → trocar → [2, 5, 3, 7, 1, 4, 9]
054: 
055: **Resultado final após passagem:**
056: **[2, 5, 3, 7, 1, 4, 9]**
057: 
058: ### **Passo 3: Análise e discussão (3 minutos)**
059: 
060: - **Perguntas para os alunos:**
061:   - Qual é o maior valor na sequência original?
062:   - Onde ele termina após a passagem?
063:   - Por que ele termina na última posição?
064:   - O que acontece com os outros valores?
065: 
066: - **Resposta esperada:**
067:   - O maior valor (9) termina na última posição.
068:   - Porque ele é "empurrado" para a direita com cada comparação, e, ao final da passagem, ele não tem mais elementos à sua direita para comparar, então fica no final.
069: 
070: ---
071: 
072: ## **III. Conclusão e Avaliação (5 minutos)**
073: 
074: - **Conclusão:**
075:   - Resumir o funcionamento da passagem de trocas adjacentes.
076:   - Destacar que, após uma passagem completa, o maior valor está na última posição, o que é a base do algoritmo de ordenação por bolha.
077: 
078: - **Avaliação:**
079:   - **Registro do vetor após cada comparação** como estratégia de avaliação.
080:   - **Entendimento do conceito de "bolha"** e da posição final do maior valor.
081:   - **Participação ativa** na simulação e discussão.
082: 
083: ---
084: 
085: ## **Material de Apoio:**
086: 
087: - **Quadro:** Para ilustrar o processo e as etapas.
088: - **Folha com sequências:** Para cada grupo.
089: - **Canetas, lápis, papel quadriculado:** Para registro das mudanças.
090: - **Exemplo de sequência:** Disponível para os alunos.
091: 
092: ---
093: 
094: ## **Recursos Adicionais (Opcional):**
095: 
096: - **Video explicativo (1 minuto):** Sobre ordenação por bolha, para reforçar o conceito.
097: - **Exercícios complementares:** Para os alunos que quiserem reforçar o tema em casa.
098: 
099: ---
100: 
101: **Nota:** Este plano pode ser adaptado para diferentes níveis e durações, dependendo da complexidade da sequência e do número de grupos.
