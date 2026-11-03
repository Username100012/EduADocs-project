001: **Plano de Aula: INNER JOIN entre clientes e pedidos**
002: 
003: ---
004: 
005: ### **1. Título da Aula**  
006: **INNER JOIN entre clientes e pedidos**
007: 
008: ---
009: 
010: ### **2. Nível Educacional**  
011: Graduação em Ciência da Computação – Formação Introductory
012: 
013: ---
014: 
015: ### **3. Duração da Aula**  
016: 50 minutos
017: 
018: ---
019: 
020: ### **4. Objetivo de Aprendizagem**  
021: Os alunos serão capazes de:  
022: - Escrever uma consulta SQL que utiliza o INNER JOIN entre as tabelas **clientes** e **pedidos**.  
023: - Identificar quais linhas serão retornadas por essa consulta.  
024: - Explicar por que clientes que não possuem pedidos não aparecerão no resultado.
025: 
026: ---
027: 
028: ### **5. Metodologia**  
029: Resolução colaborativa de problemas, com uso de exemplos práticos e discussão em grupo.
030: 
031: ---
032: 
033: ### **6. Materiais e Recursos**  
034: - Quadro de whiteboard  
035: - Folha com duas tabelas pequenas:  
036:   - **clientes**: (id_cliente, nome, email)  
037:   - **pedidos**: (id_pedido, id_cliente, data, valor)  
038: - Computadores com acesso a ambiente de programação (SQL Server, MySQL, PostgreSQL)  
039: - Perguntas guia e atividades para orientar a discussão
040: 
041: ---
042: 
043: ### **7. Estratégia de Avaliação**  
044: - Produção de consulta SQL correta com INNER JOIN.  
045: - Listagem do resultado da consulta.  
046: - Explicação clara do motivo pelo qual clientes sem pedidos não aparecem no resultado.  
047: - Participação ativa nas atividades e discussões.
048: 
049: ---
050: 
051: ### **8. Cronograma da Aula**
052: 
053: | Tempo | Atividade |
054: |-------|-----------|
055: | 0–5 minutos | **Introdução** (10 minutos): Apresentação do tópico, objetivos e contexto de INNER JOIN. |
056: | 5–15 minutos | **Explicação teórica** (15 minutos): Definição de INNER JOIN, como ele funciona, e sua aplicação em relação a clientes e pedidos. |
057: | 15–30 minutos | **Atividade prática** (20 minutos): Os alunos trabalham em grupos para escrever a consulta SQL, listam o resultado e explicam a ausência dos clientes sem pedidos. |
058: | 30–40 minutos | **Discussão em grupo** (10 minutos): Cada grupo apresenta sua consulta e explica os resultados. |
059: | 40–50 minutos | **Conclusão e revisão** (10 minutos): Revisão dos conceitos, resumo da aula, e respostas a dúvidas finais. |
060: 
061: ---
062: 
063: ### **9. Conteúdo Teórico (Resumo)**
064: 
065: **INNER JOIN** é um tipo de junção que retorna apenas as linhas que possuem valores correspondentes nas duas tabelas.  
066: - **clientes** – tabela com informações de clientes.  
067: - **pedidos** – tabela com informações de pedidos, relacionadas ao cliente por meio de uma chave estrangeira (id_cliente).  
068: - **INNER JOIN** retornará apenas os clientes que possuem pelo menos um pedido.  
069: - Clientes que não possuem pedidos não serão incluídos no resultado, pois não há correspondência nas duas tabelas.
070: 
071: ---
072: 
073: ### **10. Exemplo Prático (Tabelas)**
074: 
075: **Tabela clientes:**
076: 
077: | id_cliente | nome      | email              |
078: |------------|-----------|--------------------|
079: | 1          | João      | joao@example.com   |
080: | 2          | Maria     | maria@example.com  |
081: | 3          | Pedro     | pedro@example.com  |
082: 
083: **Tabela pedidos:**
084: 
085: | id_pedido | id_cliente | data       | valor  |
086: |-----------|------------|------------|--------|
087: | 101       | 1          | 2023-04-01 | 100.00 |
088: | 102       | 2          | 2023-04-02 | 200.00 |
089: 
090: **Consulta INNER JOIN:**
091: 
092: ```sql
093: SELECT clientes.nome, pedidos.data
094: FROM clientes
095: INNER JOIN pedidos ON clientes.id_cliente = pedidos.id_cliente;
096: ```
097: 
098: **Resultado esperado:**
099: 
100: | nome  | data       |
101: |-------|------------|
102: | João  | 2023-04-01 |
103: | Maria | 2023-04-02 |
104: 
105: **Explicação:**  
106: - João e Maria possuem pedidos, então aparecem no resultado.  
107: - Pedro não possui pedidos, então não aparece no resultado.
108: 
109: ---
110: 
111: ### **11. Perguntas para a Discussão**
112: 
113: - Por que clientes sem pedidos não aparecem no resultado do INNER JOIN?  
114: - Como você saberia se um cliente tem pedidos antes de executar a consulta?  
115: - O que aconteceria se você usasse um **LEFT JOIN** nesse caso?
116: 
117: ---
118: 
119: ### **12. Recursos Complementares (Opcionais)**  
120: - Vídeo explicativo sobre JOINs (recomendado para reforço).  
121: - Exercícios em grupo com diferentes conjuntos de dados.  
122: - Ficha de estudo com exercícios de fixação.
123: 
124: ---
125: 
126: ### **13. Conclusão da Aula**
127: 
128: - Os alunos compreenderam o funcionamento do INNER JOIN.  
129: - Concluíram que clientes sem pedidos não são incluídos no resultado.  
130: - Aprendem a escrever consultas SQL com junções e a interpretar resultados.  
131: - Estão preparados para avançar para outros tipos de JOINs, como LEFT JOIN e RIGHT JOIN.
132: 
133: ---
134: 
135: **Fim do plano de aula.**
