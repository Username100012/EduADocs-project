001: **Plano de Aula: Identificação do Maior Elemento de um Vetor Não Vazio**
002: 
003: ---
004: 
005: ### **Duração:** 50 minutos  
006: **Nível:** Graduação em Ciência da Computação  
007: **Formação:** Introductory  
008: **Tema:** Estruturas de Dados – Vetores  
009: **Objetivo de Aprendizagem:**  
010: - Implementar em pseudocódigo a identificação do maior elemento de um vetor de inteiros não vazio.  
011: - Testar valores negativos e máximos repetidos.  
012: - Aplicar a metodologia de resolução colaborativa de problemas.  
013: 
014: ---
015: 
016: ## **1. Introdução (5 minutos)**
017: 
018: - **Contextualização:**  
019:   - Vetores são estruturas de dados que armazenam uma sequência de elementos.  
020:   - O objetivo é encontrar o maior elemento em um vetor de inteiros.  
021:   - O problema é comum em algoritmos de ordenação e busca.  
022: 
023: - **Metodologia:**  
024:   - **Resolução colaborativa de problemas** – os alunos trabalharão em grupos para resolver o problema, discutindo e compartilhando ideias.  
025:   - **Recursos:**  
026:     - Quadro branco para anotações.  
027:     - Folhas com vetores de inteiros para testes de mesa.  
028: 
029: ---
030: 
031: ## **2. Explicação do Problema (5 minutos)**
032: 
033: - **Descrição do problema:**  
034:   - Dado um vetor não vazio de inteiros, encontrar o maior valor.  
035:   - O vetor pode conter valores negativos, zero e valores positivos.  
036:   - O maior elemento pode ser repetido.  
037: 
038: - **Exemplos:**  
039:   - Vetor: `[5, -3, 7, 7]` → Maior elemento: `7`  
040:   - Vetor: `[-10, -20, -5]` → Maior elemento: `-5`  
041:   - Vetor: `[1, 2, 3, 4, 5]` → Maior elemento: `5`  
042: 
043: ---
044: 
045: ## **3. Resolução Colaborativa (25 minutos)**
046: 
047: ### **Passo 1: Discutir a abordagem (5 minutos)**
048: 
049: - Os alunos discutem como identificar o maior elemento em um vetor:  
050:   - Iniciar com o primeiro elemento como "maior".  
051:   - Comparar cada elemento subsequente com o "maior".  
052:   - Se o elemento atual for maior, atualizar o "maior".  
053:   - No final, o "maior" será o resultado.  
054: 
055: ### **Passo 2: Implementar em pseudocódigo (10 minutos)**
056: 
057: - Os alunos escrevem o pseudocódigo em grupo, com base na abordagem discutida.  
058: - Exemplo de pseudocódigo:  
059: 
060: ```
061: INICIO
062:     DECLARA vetor[5] COMO INTEIRO
063:     DECLARA maior COMO INTEIRO
064:     INICIO
065:         maior = vetor[0]
066:         PARA i DE 1 A 4
067:             SE vetor[i] > maior ENTÃO
068:                 maior = vetor[i]
069:             FIM SE
070:         FIM PARA
071:     FIM
072:     IMPRIMA maior
073: FIM
074: ```
075: 
076: - **Ajustes:**  
077:   - O vetor pode ter tamanho variável, mas para simplificação, usa-se um tamanho fixo (ex: 5).  
078:   - Os alunos podem ajustar o pseudocódigo para vetores de tamanho variável, se desejado.  
079: 
080: ### **Passo 3: Testes de Mesa (10 minutos)**
081: 
082: - Os alunos usam as folhas fornecidas com vetores de inteiros para testar o pseudocódigo.  
083: - **Teste 1: Valores negativos**  
084:   - Vetor: `[-10, -5, -3, -8]`  
085:   - Esperado: `-3`  
086: - **Teste 2: Múltiplos máximos**  
087:   - Vetor: `[5, 7, 7, 5]`  
088:   - Esperado: `7`  
089: 
090: ---
091: 
092: ## **4. Avaliação (10 minutos)**
093: 
094: - **Entrega:**  
095:   - **Pseudocódigo:** Os alunos devem entregar o pseudocódigo escrito em grupo.  
096:   - **Testes de Mesa:** Os alunos devem entregar os dois testes de mesa com os resultados esperados.  
097: 
098: - **Critérios de Avaliação:**  
099:   - Correção do pseudocódigo (estrutura lógica correta).  
100:   - Correção dos testes de mesa (respostas corretas e explicações).  
101:   - Participação ativa na resolução colaborativa.  
102: 
103: ---
104: 
105: ## **5. Conclusão (5 minutos)**
106: 
107: - **Resumo do conteúdo:**  
108:   - O maior elemento de um vetor pode ser identificado com um laço que compara cada elemento com o atual "maior".  
109:   - O algoritmo funciona mesmo com valores negativos e elementos repetidos.  
110:   - A resolução colaborativa foi eficaz para desenvolver e testar o pseudocódigo.  
111: 
112: - **Próxima aula:**  
113:   - Implementação do algoritmo em linguagem de programação (ex: Python, Java).  
114:   - Aplicação em problemas reais.  
115: 
116: ---
117: 
118: **Materiais:**  
119: - Quadro branco  
120: - Folhas com vetores de inteiros  
121: - Lápis, caneta, papel  
122: 
123: **Recursos:**  
124: - Pseudocódigo  
125: - Testes de mesa  
126: 
127: --- 
128: 
129: **Nota:** Este plano de aula pode ser adaptado conforme a necessidade de aprofundamento ou nivelamento dos alunos.
