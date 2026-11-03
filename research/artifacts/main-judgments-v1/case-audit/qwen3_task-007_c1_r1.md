001: **Plano de Aula: Agrupamento SQL com GROUP BY e COUNT**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:** Escrever uma consulta SQL com GROUP BY e COUNT para contar pedidos por cliente e conferir o resultado a partir de uma tabela pequena.
007: 
008: ---
009: 
010: ## **1. Introdução (5 minutos)**
011: 
012: - **Objetivo:** Introduzir o conceito de agrupamento em SQL e a importância do GROUP BY para agrupar registros e aplicar funções agregadas como COUNT.
013: - **Contextualização:**  
014:   - Em uma base de dados, muitas linhas podem pertencer a grupos comuns (ex.: clientes, produtos, etc.).
015:   - O GROUP BY permite agrupar esses registros e aplicar funções de agregação para obter resumos.
016:   - O COUNT() conta o número de registros em cada grupo.
017: - **Material:**  
018:   - Quadro com a tabela de pedidos (exemplo simples).
019:   - Folha com identificadores de clientes (ex.: cliente_1, cliente_2, cliente_3, cliente_4).
020:   - Fichas de atividade para os alunos.
021:   - Pincel e pôster para anotações.
022: 
023: ---
024: 
025: ## **2. Explicação Teórica (10 minutos)**
026: 
027: - **Agrupamento (GROUP BY):**  
028:   - Permite agrupar registros com valores iguais em uma coluna.
029:   - Exemplo: agrupar todos os pedidos por cliente.
030: - **COUNT():**  
031:   - Função de agregação que conta o número de registros em cada grupo.
032:   - Exemplo: COUNT(*) conta todos os registros em cada grupo.
033: - **Diferença entre linhas e grupos:**  
034:   - Cada linha representa um registro individual.
035:   - Cada grupo representa um agrupamento de registros (ex.: todos os pedidos de um cliente).
036:   - A contagem de pedidos por cliente é feita por grupo, não por linha.
037: 
038: **Exemplo de consulta:**
039: ```sql
040: SELECT cliente_id, COUNT(*) AS num_pedidos
041: FROM pedidos
042: GROUP BY cliente_id;
043: ```
044: 
045: ---
046: 
047: ## **3. Atividade Colaborativa (20 minutos)**
048: 
049: **Tarefa:**  
050: - Os alunos devem escrever uma consulta SQL que conte o número de pedidos por cliente, com base na tabela de pedidos fornecida.
051: - A tabela de pedidos é apresentada no quadro com os seguintes dados:
052: 
053: | id_pedido | cliente_id |
054: |-----------|------------|
055: | 1         | cliente_1  |
056: | 2         | cliente_2  |
057: | 3         | cliente_1  |
058: | 4         | cliente_3  |
059: | 5         | cliente_2  |
060: | 6         | cliente_1  |
061: | 7         | cliente_4  |
062: | 8         | cliente_2  |
063: | 9         | cliente_3  |
064: | 10        | cliente_1  |
065: 
066: **Instruções:**
067: - Os alunos trabalham em grupos de 2 a 3 pessoas.
068: - Cada grupo deve:
069:   1. Analisar a tabela e identificar os clientes.
070:   2. Escrever a consulta SQL correta com GROUP BY e COUNT.
071:   3. Executar a consulta (simulada) e anotar o resultado.
072:   4. Comparar o resultado com a contagem manual.
073:   5. Justificar a diferença entre linhas e grupos.
074: 
075: **Resultados esperados:**
076: - **cliente_1:** 4 pedidos
077: - **cliente_2:** 3 pedidos
078: - **cliente_3:** 2 pedidos
079: - **cliente_4:** 1 pedido
080: 
081: ---
082: 
083: ## **4. Apresentação e Discussão (10 minutos)**
084: 
085: - **Cada grupo apresenta a consulta SQL que escreveu.**
086: - **Cada grupo apresenta o resultado da consulta.**
087: - **A professora comparece com o resultado esperado.**
088: - **Discutir a diferença entre linhas e grupos:**
089:   - Cada linha representa um registro (um pedido).
090:   - Cada grupo representa um cliente, e a contagem é feita por grupo.
091: - **Avaliação:**  
092:   - Correção da consulta SQL.
093:   - Correção do resultado.
094:   - Justificativa da diferença entre linhas e grupos.
095: 
096: ---
097: 
098: ## **5. Conclusão e Avaliação (5 minutos)**
099: 
100: - **Resumo:**  
101:   - O GROUP BY agrupa registros e a COUNT() conta os registros em cada grupo.
102:   - A consulta SQL deve ser escrita com base na tabela fornecida.
103:   - A diferença entre linhas e grupos está na natureza dos dados: linhas são registros individuais, grupos são agrupamentos de registros.
104: 
105: - **Avaliação:**  
106:   - A consulta SQL correta.
107:   - O resultado esperado.
108:   - A justificativa sobre a diferença entre linhas e grupos.
109: 
110: ---
111: 
112: ## **6. Recursos e Materiais Utilizados**
113: 
114: - **Quadro:** Tabela de pedidos.
115: - **Folha:** Identificadores de clientes.
116: - **Fichas de Atividade:** Para os alunos.
117: - **Pincel e Pôster:** Para anotações e apresentações.
118: 
119: ---
120: 
121: **Nota:** Esta atividade permite que os alunos compreendam a lógica do GROUP BY e COUNT, bem como a diferença entre linhas e grupos, utilizando uma abordagem prática e colaborativa.
