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
012: - **Objetivo da aula:** Introduzir os conceitos de agrupamento em SQL, com foco em GROUP BY e COUNT, e aplicá-los para contar pedidos por cliente.
013: - **Contexto:** A tabela de pedidos é uma base de dados de exemplo com identificadores de clientes e informações de pedidos.
014: - **Materiais:**  
015:   - Quadro com a tabela de pedidos (exemplo pequeno).  
016:   - Folha com identificadores de clientes.  
017:   - Páginas em branco para anotações.  
018: - **Aprendizagem esperada:**  
019:   - Compreender a diferença entre linhas e grupos.  
020:   - Escrever uma consulta SQL com GROUP BY e COUNT.  
021:   - Interpretar os resultados obtidos.  
022: 
023: ---
024: 
025: ## **2. Exemplo da Tabela (5 minutos)**
026: 
027: **Tabela: Pedidos**
028: 
029: | ID_Pedido | ID_Cliente | Data | Status |
030: |-----------|------------|------|--------|
031: | 1         | 101        | 2023-04-01 | Pendente |
032: | 2         | 102        | 2023-04-02 | Aprovado |
033: | 3         | 101        | 2023-04-03 | Pendente |
034: | 4         | 103        | 2023-04-04 | Aprovado |
035: | 5         | 102        | 2023-04-05 | Pendente |
036: | 6         | 101        | 2023-04-06 | Aprovado |
037: | 7         | 104        | 2023-04-07 | Pendente |
038: | 8         | 103        | 2023-04-08 | Aprovado |
039: | 9         | 102        | 2023-04-09 | Aprovado |
040: | 10        | 104        | 2023-04-10 | Pendente |
041: 
042: **Identificadores de clientes:**  
043: - 101  
044: - 102  
045: - 103  
046: - 104  
047: 
048: ---
049: 
050: ## **3. Explicação do Conceito (10 minutos)**
051: 
052: - **GROUP BY:** Serve para agrupar linhas com valores iguais em uma coluna.  
053: - **COUNT:** Conta o número de linhas em cada grupo.  
054: - **Diferença entre linhas e grupos:**  
055:   - **Linhas:** Cada registro da tabela é uma linha.  
056:   - **Grupos:** Quando usamos GROUP BY, agrupamos as linhas com o mesmo valor em uma coluna, resultando em grupos.  
057: - **Exemplo de consulta:**
058: 
059: ```sql
060: SELECT ID_Cliente, COUNT(*) AS Quantidade_Pedidos
061: FROM Pedidos
062: GROUP BY ID_Cliente;
063: ```
064: 
065: ---
066: 
067: ## **4. Resolução Colaborativa (20 minutos)**
068: 
069: **Passo 1: Analisar a tabela de pedidos.**  
070: - Os alunos devem identificar os ID_Cliente e contar quantos pedidos cada cliente tem.  
071: - Ajudar os alunos a entender a estrutura da tabela e a identificar os grupos (por ID_Cliente).  
072: 
073: **Passo 2: Escrever a consulta SQL.**  
074: - Os alunos devem escrever a consulta SQL com GROUP BY e COUNT, usando a tabela de pedidos.  
075: - Ajudar os alunos a corrigir erros, se houver.  
076: 
077: **Passo 3: Executar a consulta e verificar o resultado.**  
078: - Os alunos devem verificar a saída da consulta e comparar com o resultado esperado.  
079: - Comparar com a tabela de pedidos para confirmar a contagem.  
080: 
081: **Passo 4: Justificar a diferença entre linhas e grupos.**  
082: - Os alunos devem explicar por que a consulta retorna grupos e não linhas.  
083: - Comparar a quantidade de linhas com a quantidade de grupos.  
084: 
085: ---
086: 
087: ## **5. Avaliação (5 minutos)**
088: 
089: - **Questão 1:** Escreva a consulta SQL para contar os pedidos por cliente.  
090: - **Questão 2:** Qual é a quantidade de pedidos de cada cliente?  
091: - **Questão 3:** Justifique a diferença entre o número de linhas da tabela e o número de grupos.  
092: 
093: **Resposta esperada para a consulta:**
094: 
095: ```sql
096: SELECT ID_Cliente, COUNT(*) AS Quantidade_Pedidos
097: FROM Pedidos
098: GROUP BY ID_Cliente;
099: ```
100: 
101: **Resultado esperado:**
102: 
103: | ID_Cliente | Quantidade_Pedidos |
104: |------------|--------------------|
105: | 101        | 3                  |
106: | 102        | 3                  |
107: | 103        | 2                  |
108: | 104        | 2                  |
109: 
110: **Justificativa:**  
111: - A tabela tem 10 linhas.  
112: - O GROUP BY agrupa as linhas por ID_Cliente, resultando em 4 grupos.  
113: - Cada grupo representa um cliente, e o COUNT conta quantos pedidos cada cliente tem.  
114: 
115: ---
116: 
117: ## **6. Conclusão (5 minutos)**
118: 
119: - **Resumo da aula:**  
120:   - GROUP BY e COUNT são ferramentas essenciais para agrupar dados e contar registros.  
121:   - A consulta SQL deve ser escrita com atenção para agrupar corretamente.  
122:   - A diferença entre linhas e grupos é fundamental para entender a estrutura dos dados.  
123: - **Perguntas para reflexão:**  
124:   - Por que usamos GROUP BY?  
125:   - Como a consulta pode ser ajustada se houver mais clientes?  
126: - **Próxima aula:** Trabalhar com filtros (WHERE) e ordenação (ORDER BY).  
127: 
128: ---
129: 
130: ## **Materiais para Entrega**
131: 
132: - **Consulta SQL correta.**  
133: - **Resultado esperado da consulta.**  
134: - **Explicação da diferença entre linhas e grupos.**  
135: 
136: ---
137: 
138: **Nota:** A aula foi estruturada com base em um exemplo pequeno para facilitar a compreensão, mas pode ser adaptada para tabelas maiores, conforme necessário.
