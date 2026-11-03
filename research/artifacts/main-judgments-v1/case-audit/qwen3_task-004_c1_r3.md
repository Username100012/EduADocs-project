001: **Plano de Aula: Operações de Pilha com Política LIFO**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Objetivo de Aprendizagem:** Simular operações **push** e **pop** em uma pilha, identificar o **topo** e o **estado da pilha** após cada operação, incluindo a **remoção em pilha vazia**.  
006: **Metodologia:** Resolução colaborativa de problemas  
007: **Recursos:**  
008: - Quadro de whiteboard  
009: - Folha de atividade com sequências de operações de pilha  
010: - Caneta, lápis e papel para os alunos  
011: 
012: ---
013: 
014: ## **1. Introdução (5 minutos)**
015: 
016: **Objetivo:** Introduzir o conceito de pilha e sua política LIFO (Last In, First Out).
017: 
018: - **Definição de pilha:** Estrutura de dados linear que permite inserção e remoção de elementos em apenas um extremo (topo da pilha).
019: - **Política LIFO:** O último elemento inserido será o primeiro a ser removido.
020: - **Exemplo:** Pilha de pratos: o último prato colocado no topo será o primeiro a ser retirado.
021: 
022: **Perguntas para estimular o pensamento:**
023: - Qual a diferença entre uma pilha e uma fila?
024: - Como a pilha é usada em computação (ex: chamadas de funções, histórico de navegação)?
025: 
026: ---
027: 
028: ## **2. Explicação Teórica (10 minutos)**
029: 
030: **Conteúdo:**
031: - **Operações básicas:**
032:   - **push:** Inserir um elemento no topo da pilha.
033:   - **pop:** Remover o elemento do topo da pilha.
034:   - **top:** Obter o elemento no topo da pilha (sem remover).
035:   - **isEmpty:** Verificar se a pilha está vazia.
036: - **Estado da pilha:** Representar a pilha como uma lista ou um array, indicando o topo.
037: - **Erro em pilha vazia:** Se tentar pop em uma pilha vazia, deve-se tratar como erro ou retornar uma mensagem de erro.
038: 
039: **Exemplo de representação:**
040: - Pilha: [1, 2, 3] → topo = 3
041: - Pilha vazia: [] → topo = null, isEmpty = true
042: 
043: ---
044: 
045: ## **3. Atividade Colaborativa (25 minutos)**
046: 
047: **Objetivo:** Os alunos trabalham em grupos de 2-3 pessoas, simulando operações de pilha com base em uma sequência fornecida.
048: 
049: **Recursos fornecidos:**
050: - Folha com uma sequência de operações (exemplo abaixo):
051: 
052: > **Sequência de operações:**
053: > 1. push(10)
054: > 2. push(20)
055: > 3. push(30)
056: > 4. pop()
057: > 5. top()
058: > 6. pop()
059: > 7. pop()
060: > 8. isEmpty()
061: > 9. push(40)
062: > 10. top()
063: 
064: **Instruções para os alunos:**
065: - Usar o quadro de whiteboard para rastrear as operações.
066: - Cada grupo deve indicar:
067:   - O estado da pilha após cada operação.
068:   - O valor do topo (se existir).
069:   - O resultado da operação (ex: "pop() retornou 30", "isEmpty() retornou false").
070: - Se a pilha estiver vazia, indicar que a operação pop resultou em erro ou em uma mensagem de erro.
071: 
072: **Avaliação:**
073: - Cada grupo deve apresentar o rastreamento de operações no quadro.
074: - O professor verifica a correção das operações e corrigi as falhas.
075: - O aluno que fornece a resposta correta para a operação "pop() em pilha vazia" será premiado com uma pontuação adicional.
076: 
077: ---
078: 
079: ## **4. Conclusão e Refletir (10 minutos)**
080: 
081: **Resumo:**
082: - Revisar as operações push e pop com a política LIFO.
083: - Destacar a importância de verificar se a pilha está vazia antes de realizar uma pop.
084: - Discutir situações reais onde as pilhas são usadas (ex: chamadas de funções, histórico de navegação, back-end de aplicações).
085: 
086: **Perguntas de reflexão:**
087: - O que aconteceria se tentássemos pop() em uma pilha vazia?
088: - Como a pilha é usada em um sistema de chamadas de funções?
089: - Qual a vantagem de usar uma pilha em vez de uma fila?
090: 
091: **Avaliação final:**
092: - O professor observa o desempenho dos alunos na simulação.
093: - O aluno que respondeu corretamente sobre a pilha vazia recebe uma pontuação adicional.
094: - A atividade é avaliada com base na precisão no rastreamento das operações e na participação.
095: 
096: ---
097: 
098: ## **5. Recursos de Aprendizagem Complementar (opcional)**
099: 
100: - **Exercícios em Python:**
101:   ```python
102:   class Pilha:
103:       def __init__(self):
104:           self.items = []
105: 
106:       def push(self, item):
107:           self.items.append(item)
108: 
109:       def pop(self):
110:           if self.isEmpty():
111:               raise Exception("Pilha vazia")
112:           return self.items.pop()
113: 
114:       def top(self):
115:           if self.isEmpty():
116:               return None
117:           return self.items[-1]
118: 
119:       def isEmpty(self):
120:           return len(self.items) == 0
121:   ```
122: 
123: - **Link para video explicativo (opcional):** [YouTube - Pilha LIFO - Exemplo Simples]
124: 
125: ---
126: 
127: **Nota:** Este plano de aula pode ser adaptado para diferentes níveis de dificuldade, incluindo a implementação em linguagens de programação.
