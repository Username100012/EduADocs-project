001: **Plano de Aula: Agrupamento SQL com GROUP BY e COUNT**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:** Escrever uma consulta SQL com GROUP BY e COUNT para contar pedidos por cliente e conferir o resultado com base em uma tabela pequena.
007: 
008: ---
009: 
010: ## **1. Introdução (5 minutos)**
011: 
012: - **Objetivo:** Introduzir o conceito de agrupamento em SQL e a importância do GROUP BY para agrupar registros e aplicar funções agregadas como COUNT().
013: - **Conteúdo:**
014:   - Definição de agrupamento em SQL.
015:   - Função COUNT() e seu uso em consultas.
016:   - O papel do GROUP BY para agrupar resultados.
017: - **Materiais:**  
018:   - Quadro com a tabela de pedidos (com colunas: `id_pedido`, `id_cliente`, `data_pedido`).
019:   - Folha com os identificadores de clientes (ex: 1, 2, 3, 4, 5).
020:   - Perguntas guia para estimular a reflexão.
021: 
022: ---
023: 
024: ## **2. Aprendizagem Ativa (20 minutos)**
025: 
026: ### **Aula 1: Revisão da Tabela de Pedidos**
027: 
028: - **Tarefa:** O professor apresenta a tabela de pedidos com 10 registros, com os seguintes campos:
029:   - `id_pedido` (chave primária)
030:   - `id_cliente` (chave estrangeira)
031:   - `data_pedido` (data do pedido)
032: 
033: - **Exemplo de dados:**
034: 
035: | id_pedido | id_cliente | data_pedido  |
036: |-----------|------------|--------------|
037: | 1         | 1          | 2024-01-10   |
038: | 2         | 2          | 2024-01-11   |
039: | 3         | 1          | 2ity-01-12   |
040: | 4         | 3          | 2024-01-13   |
041: | 5         | 2          | 2024-01-14   |
042: | 6         | 4          | 2024-01-15   |
043: | 7         | 1          | 2024-01-16   |
044: | 8         | 3          | 2024-01-17   |
045: | 9         | 2          | 2024-01-18   |
046: | 10        | 4          | 2024-01-19   |
047: 
048: - **Questão:** Quantos pedidos cada cliente fez?
049: 
050: ### **Aula 2: Resolução Colaborativa**
051: 
052: - **Grupos de 3 a 4 alunos.**
053: - **Tarefa:** Cada grupo deve escrever uma consulta SQL para contar os pedidos por cliente.
054: - **Dica:** Use `GROUP BY id_cliente` e `COUNT(id_pedido)`.
055: - **Exemplo de consulta:**
056: 
057: ```sql
058: SELECT id_cliente, COUNT(id_pedido) AS num_pedidos
059: FROM pedidos
060: GROUP BY id_cliente;
061: ```
062: 
063: - **Orientação do professor:**  
064:   - Incentivar a criação da consulta.
065:   - Verificar se os alunos usaram corretamente o GROUP BY.
066:   - Apresentar a consulta em um quadro para todos os grupos observarem.
067: 
068: ---
069: 
070: ## **3. Avaliação e Conferência (15 minutos)**
071: 
072: ### **Passo 1: Executar a Consulta**
073: 
074: - O professor executa a consulta SQL e apresenta o resultado no quadro.
075: 
076: ### **Passo 2: Comparar com a Tabela**
077: 
078: - Cada grupo analisa o resultado e compara com a tabela de pedidos.
079: - Exemplo de resultado esperado:
080: 
081: | id_cliente | num_pedidos |
082: |------------|-------------|
083: | 1          | 3           |
084: | 2          | 3           |
085: | 3          | 2           |
086: | 4          | 2           |
087: 
088: ### **Passo 3: Justificar a Diferença entre Linhas e Grupos**
089: 
090: - **Questão:** Por que o resultado tem 4 linhas, mas apenas 4 clientes?
091: - **Resposta Esperada:**  
092:   - A consulta agrupa os registros por `id_cliente`, então cada linha representa um cliente único.
093:   - A tabela tem 10 registros, mas 4 clientes distintos.
094: 
095: ### **Passo 4: Discussão Final**
096: 
097: - **Perguntas de reflexão:**
098:   - Por que usamos GROUP BY?
099:   - O que acontece se não usarmos GROUP BY?
100:   - Como saber quantos clientes distintos existem?
101: 
102: ---
103: 
104: ## **4. Conclusão e Extensão (10 minutos)**
105: 
106: - **Resumo:**  
107:   - GROUP BY é usado para agrupar registros com valores repetidos.
108:   - COUNT() conta o número de registros em cada grupo.
109:   - A consulta final mostra o número de pedidos por cliente.
110:   
111: - **Extensão (opcional):**  
112:   - Incentivar os alunos a criar uma consulta com `HAVING` para filtrar clientes com mais de 2 pedidos.
113:   - Apresentar a consulta e o resultado esperado.
114: 
115: - **Dúvidas?**  
116:   - O professor responde perguntas individuais ou coletivas.
117: 
118: ---
119: 
120: ## **Materiais Utilizados**
121: 
122: - **Quadro:** Tabela de pedidos (10 registros).
123: - **Folha:** Identificadores de clientes (1, 2, 3, 4, 5).
124: - **Dinâmica de grupo:** Resolução colaborativa com orientação do professor.
125: 
126: ---
127: 
128: ## **Avaliação**
129: 
130: - **Estratégia:**  
131:   - A consulta SQL correta e a justificativa sobre a diferença entre linhas e grupos.
132:   - Participação ativa em grupos e em discussões.
133: - **Avaliação por desempenho:**  
134:   - A consulta correta e o entendimento do GROUP BY e COUNT() são os critérios principais.
135: 
136: ---
137: 
138: **Nota Final:** Este plano de aula combina teoria, prática e colaboração, permitindo que os alunos compreendam e aplicem o conceito de agrupamento em SQL de forma prática e contextualizada.
