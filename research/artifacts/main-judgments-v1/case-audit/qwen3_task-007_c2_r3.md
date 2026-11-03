001: **PLANO DE AULA – Agrupamento SQL com GROUP BY e COUNT**
002: 
003: ---
004: 
005: ### **1. Título da aula**  
006: **Agrupamento SQL com GROUP BY e COUNT – Contagem de Pedidos por Cliente**
007: 
008: ---
009: 
010: ### **2. Nível educacional**  
011: Graduação em Ciência da Computação – Formação introdutória em SQL
012: 
013: ---
014: 
015: ### **3. Duração**  
016: 50 minutos
017: 
018: ---
019: 
020: ### **4. Objetivo de aprendizagem**  
021: O aluno será capaz de escrever uma consulta SQL que utilize o comando `GROUP BY` e `COUNT` para contar os pedidos por cliente, e verificar o resultado com base em uma tabela de pedidos e identificadores de clientes.
022: 
023: ---
024: 
025: ### **5. Metodologia**  
026: **Resolução colaborativa de problemas**  
027: Aula prática com orientação do professor, com participação ativa dos alunos, resolução de problemas em grupo e apresentação de resultados.
028: 
029: ---
030: 
031: ### **6. Materiais e recursos**  
032: - Quadro de whiteboard  
033: - Folha com a tabela de pedidos (com colunas: `id_pedido`, `id_cliente`, `data_pedido`, `valor`)  
034: - Folha com identificadores de clientes (ex: `cliente_1`, `cliente_2`, `cliente_3`)  
035: - Páginas com exemplos de consultas SQL  
036: - Pincel e giz para anotações  
037: - Computadores ou tablets com acesso a banco de dados (opcional, se a aula for teórico-prática)
038: 
039: ---
040: 
041: ### **7. Estratégia de avaliação**  
042: - Entrega de uma consulta SQL que use `GROUP BY` e `COUNT` para contar os pedidos por cliente  
043: - Justificar a diferença entre linhas e grupos (ex: linha por cliente, grupo por cliente)  
044: - Análise de resultados obtidos com a tabela fornecida
045: 
046: ---
047: 
048: ### **8. Estructura da aula**
049: 
050: #### **I. Introdução (5 minutos)**  
051: - Apresentar o conceito de agrupamento em SQL.  
052: - Explicar o uso do `GROUP BY` e `COUNT` para agrupar registros e contar valores.  
053: - Mostrar a importância de agrupar dados para análise de dados.  
054: - Apresentar a tabela de pedidos e os identificadores de clientes.
055: 
056: #### **II. Aprendizagem direta (10 minutos)**  
057: - Explicar o funcionamento do `GROUP BY` e `COUNT` com exemplos.  
058: - Exibir uma consulta SQL de exemplo:  
059:   ```sql
060:   SELECT id_cliente, COUNT(*) AS quantidade_pedidos
061:   FROM pedidos
062:   GROUP BY id_cliente;
063:   ```  
064: - Discutir como essa consulta agrupa os pedidos por cliente e conta os registros em cada grupo.
065: 
066: #### **III. Atividade prática (20 minutos)**  
067: - Dividir os alunos em grupos de 2 a 3 pessoas.  
068: - Distribuir a tabela de pedidos e os identificadores de clientes.  
069: - Cada grupo deve escrever uma consulta SQL para contar os pedidos por cliente.  
070: - Os grupos devem:  
071:   1. Verificar a tabela e identificar quais clientes existem.  
072:   2. Escrever a consulta SQL com `GROUP BY` e `COUNT`.  
073:   3. Executar a consulta (ou simular o resultado) e comparar com a tabela.  
074:   4. Justificar a diferença entre linhas e grupos.
075: 
076: #### **IV. Apresentação e discussão (10 minutos)**  
077: - Cada grupo apresenta sua consulta e resultado.  
078: - O professor corrigir e explicar os pontos importantes.  
079: - Discutir a diferença entre linhas e grupos (ex: cada linha representa um cliente, cada grupo também representa um cliente, mas o `GROUP BY` agrupa os registros, não as linhas).  
080: - Destacar a importância de usar `GROUP BY` para agrupar dados antes de fazer contagens.
081: 
082: #### **V. Conclusão e avaliação (5 minutos)**  
083: - Revisar os conceitos principais: `GROUP BY`, `COUNT`, agrupamento e contagem.  
084: - Entregar a consulta SQL e a contagem esperada para cada cliente.  
085: - Perguntas de fixação:  
086:   - O que acontece se não usar `GROUP BY` na consulta?  
087:   - Como a consulta diferenciará linhas e grupos?  
088:   - Por que usar `GROUP BY` com `COUNT` é útil para análise de dados?
089: 
090: ---
091: 
092: ### **9. Recursos complementares (opcional)**  
093: - Exercícios em banco de dados (ex: MySQL, PostgreSQL)  
094: - Vídeo explicativo sobre `GROUP BY` e `COUNT` (para reforço)
095: 
096: ---
097: 
098: ### **10. Avaliação**  
099: - A entrega da consulta SQL com justificativa  
100: - A capacidade de identificar a diferença entre linhas e grupos  
101: - A compreensão do uso de `GROUP BY` e `COUNT` para análise de dados
102: 
103: ---
104: 
105: ### **11. Referências (opcional)**  
106: - Livro: *SQL para Dummies* – por Allen G. Morgan  
107: - Site: https://www.w3schools.com/sql/sql_groupby.asp
108: 
109: --- 
110: 
111: **Fim do plano de aula.**
