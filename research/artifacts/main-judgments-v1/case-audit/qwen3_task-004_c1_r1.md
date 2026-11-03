001: **Plano de Aula: Operações de Pilha com Política LIFO**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Objetivo de Aprendizagem:** Simular operações **push** e **pop** em uma pilha, identificar o **topo** e o **estado da pilha** após cada operação, incluindo a **remoção em pilha vazia**.  
006: **Metodologia:** Resolução colaborativa de problemas  
007: **Recursos:** Quadro de whiteboard, folha com sequências de operações de pilha, lápis, caneta, papel
008: 
009: ---
010: 
011: ### **I. Introdução (5 minutos)**
012: 
013: **Objetivo:** Introduzir o conceito de pilha e sua política LIFO (Last In, First Out).
014: 
015: - **Definição de pilha:** Estrutura de dados linear onde os elementos são inseridos e removidos do **topo**.
016: - **Política LIFO:** O último elemento inserido é o primeiro a ser removido.
017: - **Exemplo de uso:** Pilhas são usadas em linguagem de montagem, backtracking, chamadas de funções, etc.
018: - **Apresentar o conceito de topo e estado da pilha** (vazia, com 1 elemento, com vários elementos).
019: 
020: **Apoio visual:** Desenhar uma pilha simples no quadro (exemplo: [1, 2, 3] – topo = 3).
021: 
022: ---
023: 
024: ### **II. Atividade de Introdução (10 minutos)**
025: 
026: **Objetivo:** Introduzir as operações **push** e **pop** e suas consequências.
027: 
028: - **Explicar:**
029:   - **push(x):** Insere o elemento **x** no topo da pilha.
030:   - **pop():** Remove o elemento do topo da pilha. Se a pilha estiver vazia, gera uma exceção ou mensagem de erro.
031:   - **top():** Retorna o elemento no topo da pilha (sem removê-lo).
032:   - **isEmpty():** Verifica se a pilha está vazia.
033: 
034: **Exemplo de operações:**
035: 1. push(1)
036: 2. push(2)
037: 3. top()
038: 4. pop()
039: 5. push(3)
040: 6. pop()
041: 7. pop()
042: 8. isEmpty()
043: 
044: **Apoio visual:** Mostrar no quadro a sequência de operações e o estado da pilha após cada passo.
045: 
046: ---
047: 
048: ### **III. Atividade Colaborativa (25 minutos)**
049: 
050: **Objetivo:** Simular operações de pilha com base em uma sequência fornecida, usando o quadro e folha.
051: 
052: **Instruções:**
053: 
054: 1. **Distribuir para os alunos uma folha com uma sequência de operações de pilha** (exemplo:  
055:    ```
056:    push(10)
057:    push(20)
058:    push(30)
059:    pop()
060:    pop()
061:    push(40)
062:    pop()
063:    pop()
064:    isEmpty()
065:    ``)
066: 
067: 2. **Os alunos trabalham em grupos de 3 a 4 pessoas**, com a tarefa de:
068:    - Simular a pilha em papel.
069:    - Registrar o estado da pilha após cada operação (topo, elementos, vazia?).
070:    - Identificar se houve **erro de remoção em pilha vazia**.
071: 
072: 3. **Apoio visual:** Usar o quadro para mostrar o rastreamento das operações, enquanto os alunos trabalham em grupo.
073: 
074: **Exemplo de resposta esperada:**
075: 
076: | Operação | Estado da Pilha |
077: |----------|------------------|
078: | push(10) | [10] (topo=10) |
079: | push(20) | [10,20] (topo=20) |
080: | push(30) | [10,20,30] (topo=30) |
081: | pop()    | [10,20] (topo=20) |
082: | pop()    | [10] (topo=10) |
083: | push(40) | [10,40] (topo=40) |
084: | pop()    | [10] (topo=10) |
085: | pop()    | [] (vazia) |
086: | isEmpty()| true            |
087: 
088: **Reforço:** Discutir os erros de remoção em pilha vazia e como lidar com eles (ex: mensagem de erro ou exceção).
089: 
090: ---
091: 
092: ### **IV. Conclusão e Avaliação (10 minutos)**
093: 
094: **Objetivo:** Reforçar o entendimento e avaliar a aplicação das operações de pilha.
095: 
096: - **Perguntas de reflexão:**
097:   - O que acontece se tentarmos pop() em uma pilha vazia?
098:   - Como a pilha se comporta com várias operações push e pop?
099:   - Qual é o significado do topo da pilha?
100: 
101: - **Avaliação por rastreamento:**
102:   - Cada grupo apresenta o rastreamento das operações (quadro e folha).
103:   - Professor verifica se os alunos identificaram corretamente o topo e o estado da pilha.
104:   - O professor também avalia se os alunos identificaram a remoção em pilha vazia.
105: 
106: **Feedback:**
107: - Destaca os pontos fortes e corrigem os erros comuns.
108: - Resumir o conceito de pilha e seu uso em algoritmos.
109: 
110: ---
111: 
112: ### **V. Recomendação de Próximos Passos**
113: 
114: - Trabalhar com exemplos práticos em linguagens de programação (Python, C++, Java).
115: - Introduzir a pilha como estrutura de dados em algoritmos (ex: pilha de chamadas de função).
116: - Trabalhar com problemas de simulação de pilhas em contextos reais.
117: 
118: ---
119: 
120: **Material de apoio:**
121: - Folha com sequências de operações de pilha.
122: - Caneta, lápis, papel.
123: - Quadro de whiteboard.
124: 
125: ---
126: 
127: **Nota:** Este plano pode ser adaptado com base no nível de conhecimento dos alunos e no tempo de aula disponível.
