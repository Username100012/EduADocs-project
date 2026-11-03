001: **Plano de Aula: INNER JOIN entre Clientes e Pedidos**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introdutória  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:**  
007: - Escrever uma consulta SQL com INNER JOIN entre as tabelas **clientes** e **pedidos**.  
008: - Determinar quais linhas são retornadas quando um cliente não possui pedidos.  
009: - Entender o funcionamento do INNER JOIN e a diferença entre INNER JOIN e outros tipos de JOIN.  
010: 
011: ---
012: 
013: ### **1. Introdução (5 minutos)**
014: 
015: **Objetivo:** Estabelecer o contexto da aula e motivar os alunos para a atividade.  
016: 
017: - Apresentar as tabelas **clientes** e **pedidos** como exemplos de tabelas relacionadas em uma base de dados.  
018: - Explicar o conceito de JOIN, especialmente o INNER JOIN, como maneira de combinar registros de duas tabelas com base em uma coluna comum.  
019: - Perguntar: "Como você acha que os dados de clientes e pedidos estão relacionados?"  
020: - Mostrar o **quadro de tabelas** com exemplos pequenos de clientes e pedidos.  
021: 
022: ---
023: 
024: ### **2. Aprendizagem Direta (10 minutos)**
025: 
026: **Objetivo:** Introduzir o conceito de INNER JOIN e explicar como ele funciona.  
027: 
028: - Explicar que o INNER JOIN retorna apenas as linhas que têm correspondência em ambas as tabelas.  
029: - Mostrar um exemplo de consulta SQL com INNER JOIN.  
030: - Apresentar a **tabela clientes** e a **tabela pedidos** com exemplos fictícios.  
031: 
032: **Exemplo de tabelas:**
033: 
034: **Tabela clientes:**
035: 
036: | ClienteID | Nome        | Endereço        |
037: |-----------|-------------|-----------------|
038: | 1         | João Silva  | Rua A, 123      |
039: | 2         | Maria Souza | Rua B, 456      |
040: | 3         | Carlos Pereira | Rua C, 789     |
041: 
042: **Tabela pedidos:**
043: 
044: | PedidoID | ClienteID | Data         | Valor |
045: |----------|-----------|--------------|-------|
046: | 101      | 1         | 2023-04-01  | 100   |
047: | 102      | 2         | 2023-04-02  | 150   |
048: | 103      | 3         | 2ity-04-03  | 200   |
049: 
050: **Explicação:**  
051: - O INNER JOIN combina as linhas de clientes com as linhas de pedidos com base no **ClienteID**.  
052: - Apenas os clientes que têm pelo menos um pedido serão retornados.  
053: - Clientes sem pedidos **não serão incluídos** no resultado.  
054: 
055: ---
056: 
057: ### **3. Atividade Colaborativa (25 minutos)**
058: 
059: **Objetivo:** Os alunos trabalham em grupos para escrever a consulta SQL e determinar as linhas retornadas.
060: 
061: **Passos da Atividade:**
062: 
063: 1. **Distribuir as tabelas:**  
064:    - Cada grupo recebe uma cópia do **quadro de tabelas** com as tabelas **clientes** e **pedidos**.  
065:    - Os alunos devem analisar as tabelas e identificar quais clientes têm pedidos.
066: 
067: 2. **Escrever a consulta SQL:**  
068:    - Cada grupo deve escrever uma consulta SQL com INNER JOIN entre as duas tabelas.  
069:    - Exemplo:  
070:      ```sql
071:      SELECT clientes.Nome, pedidos.Data
072:      FROM clientes
073:      INNER JOIN pedidos ON clientes.ClienteID = pedidos.ClienteID;
074:      ```
075: 
076: 3. **Executar a consulta e listar resultados:**  
077:    - Os alunos devem executar a consulta e listar as linhas retornadas.  
078:    - Identificar quais clientes estão presentes no resultado.  
079: 
080: 4. **Discutir a ausência de clientes sem pedidos:**  
081:    - Perguntar: "Por que alguns clientes não aparecem no resultado?"  
082:    - Explicar que o INNER JOIN ignora os clientes que não possuem registros na tabela de pedidos.  
083: 
084: 5. **Comparar com um JOIN LEFT (como estratégia de avaliação):**  
085:    - Incentivar os alunos a refletir: "Se quisessem incluir todos os clientes, mesmo que não tenham pedidos, qual seria o tipo de JOIN?"  
086:    - Introduzir o LEFT JOIN como alternativa para avaliação.  
087: 
088: ---
089: 
090: ### **4. Avaliação (5 minutos)**
091: 
092: **Objetivo:** Verificar o entendimento do INNER JOIN e a capacidade de escrever uma consulta correta.
093: 
094: - **Perguntas de avaliação:**
095:   1. Qual é a diferença entre INNER JOIN e LEFT JOIN?
096:   2. Por que alguns clientes não aparecem no resultado da consulta?
097:   3. Escreva uma consulta que inclua todos os clientes, mesmo que não tenham pedidos.
098: 
099: - **Resposta esperada:**
100:   - INNER JOIN retorna apenas os clientes com pedidos.  
101:   - LEFT JOIN inclui todos os clientes, mesmo sem pedidos.  
102:   - Exemplo de consulta com LEFT JOIN:  
103:     ```sql
104:     SELECT clientes.Nome, pedidos.Data
105:     FROM clientes
106:     LEFT JOIN pedidos ON clientes.ClienteID = pedidos.ClienteID;
107:     ```
108: 
109: ---
110: 
111: ### **5. Conclusão e Reflexão (5 minutos)**
112: 
113: **Objetivo:** Consolidar o aprendizado e motivar para a próxima aula.
114: 
115: - Resumir os conceitos principais:  
116:   - INNER JOIN retorna apenas os clientes com pedidos.  
117:   - LEFT JOIN inclui todos os clientes.  
118: - Perguntar: "Como você usaria o INNER JOIN em um projeto real?"  
119: - Encerrar com uma pergunta de reflexão: "Por que é importante entender a diferença entre os tipos de JOIN?"
120: 
121: ---
122: 
123: ### **Recursos Utilizados:**
124: 
125: - Quadro com tabelas **clientes** e **pedidos**  
126: - Folhas com dados fictícios para os alunos  
127: - Pincel e quadro branco para anotações  
128: - Computadores ou tablets para execução de consultas SQL (opcional)  
129: 
130: ---
131: 
132: **Nota:** Este plano de aula pode ser adaptado para usar ferramentas como MySQL Workbench, SQL Server Management Studio, ou até mesmo um ambiente online como DB Fiddle para a execução das consultas.
