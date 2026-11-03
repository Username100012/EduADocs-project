001: **Plano de Aula: Operações de Pilha com Política LIFO**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Recursos:** Quadro, folha com sequências de operações de pilha, canetas, lápis, marcadores, papel de rascunho
007: 
008: ---
009: 
010: ### **Objetivo de Aprendizagem:**
011: Simular operações **push** e **pop** em uma pilha com política LIFO (Last In, First Out), identificar o **topo** da pilha após cada operação e tratar corretamente a remoção de elementos de uma pilha vazia.
012: 
013: ---
014: 
015: ### **Conteúdo Teórico (5 minutos):**
016: 
017: 1. **Definição de Pilha:**
018:    - Estrutura de dados linear que segue a política **LIFO** (último a entrar, primeiro a sair).
019:    - Operações principais: **push** (inserir), **pop** (remover), **top** (consultar o elemento no topo).
020:    - Pilha pode estar em **estado vazio** ou **com elementos**.
021: 
022: 2. **Operações:**
023:    - **push(x)**: Adiciona um elemento **x** no topo da pilha.
024:    - **pop()**: Remove o elemento do topo da pilha. Se a pilha estiver vazia, lança uma exceção ou retorna um valor especial (como `None` ou `Error`).
025:    - **top()**: Retorna o elemento no topo da pilha, sem removê-lo.
026: 
027: 3. **Exemplo de Pilha:**
028:    ```
029:    [1, 2, 3] → topo = 3
030:    [1, 2] → topo = 2
031:    [] → pilha vazia
032:    ```
033: 
034: ---
035: 
036: ### **Atividade Prática (35 minutos):**
037: 
038: **Instruções:**
039: 
040: - Divida a turma em grupos de 3 a 4 alunos.
041: - Distribua a cada grupo uma **folha com uma sequência de operações** (exemplo abaixo).
042: - Cada grupo deve **simular** as operações em uma pilha, mantendo o **topo** atualizado após cada operação.
043: - Use um **quadro** para mostrar a pilha em tempo real (opcional, se houver).
044: 
045: ---
046: 
047: ### **Exemplo de Sequência de Operações (para cada grupo):**
048: 
049: | Operação | Valor | Estado da Pilha | Topo |
050: |----------|-------|------------------|------|
051: | push(10) | 10    | [10]             | 10   |
052: | push(20) | 20    | [10, 20]         | 20   |
053: | push(30) | 30    | [10, 20, 30]     | 30   |
054: | pop()    |       | [10, 20]         | 20   |
055: | pop()    |       | [10]             | 10   |
056: | pop()    |       | []               | —    |
057: | top()    |       | —                | —    |
058: | push(40) | 40    | [40]             | 40   |
059: 
060: ---
061: 
062: ### **Estratégia de Avaliação (10 minutos):**
063: 
064: 1. **Rastreamento de Operações:**
065:    - Cada grupo deve **anotar** o estado da pilha e o topo após cada operação.
066:    - No final, apresentar o resultado final da pilha e o valor do topo (se houver).
067: 
068: 2. **Tratamento de Pilha Vazia:**
069:    - O grupo deve **identificar** a operação que tenta remover de uma pilha vazia e explicar como seria o resultado (ex: erro ou retorno de `None`).
070: 
071: 3. **Discussão Coletiva:**
072:    - Cada grupo apresenta suas respostas.
073:    - Discutir os pontos de atenção:
074:      - Como identificar o topo da pilha.
075:      - Como tratar a remoção de uma pilha vazia.
076:      - Como manter a ordem correta dos elementos.
077: 
078: ---
079: 
080: ### **Encerramento (5 minutos):**
081: 
082: - **Resumo:**
083:   - Relembrar a importância da política LIFO e como as operações **push** e **pop** afetam a pilha.
084:   - Destacar a importância do **topo** e do **estado da pilha** em algoritmos e aplicações.
085: - **Perguntas de Refletência:**
086:   - O que acontece se tentarmos pop() de uma pilha vazia?
087:   - Como podemos usar pilhas em aplicações práticas (ex: histórico de navegação, backtracking, etc.)?
088: 
089: ---
090: 
091: ### **Recursos Necessários:**
092: 
093: - Quadro de whiteboard (ou papel quadriculado)
094: - Folhas com sequências de operações
095: - Canetas, lápis, marcadores
096: - Papel de rascunho (opcional)
097: 
098: ---
099: 
100: ### **Avaliação Formativa:**
101: 
102: - **Participação ativa** na resolução colaborativa.
103: - **Correção das operações** em pilha.
104: - **Identificação correta** do topo e do estado da pilha.
105: - **Tratamento adequado** de pilhas vazias.
106: 
107: ---
108: 
109: **Nota:** Este plano de aula pode ser adaptado para diferentes níveis de dificuldade, incluindo a implementação de pilhas em linguagens de programação (Python, Java, C++), dependendo do contexto da aula.
