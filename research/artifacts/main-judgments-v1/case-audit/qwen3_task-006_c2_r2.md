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
023: - Identificar quais linhas serão retornadas pela consulta.  
024: - Explicar por que clientes que não possuem pedidos não aparecerão nos resultados.
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
035: - Folha com duas tabelas pequenas: **clientes** e **pedidos**  
036: - Pincel e giz de quadro  
037: - Cartões de perguntas para estimular a discussão  
038: - Computadores ou tablets com acesso a ambiente de programação (opcional)
039: 
040: ---
041: 
042: ### **7. Estratégia de Avaliação**  
043: - Produção de uma consulta SQL correta com INNER JOIN  
044: - Listagem do resultado esperado da consulta  
045: - Explicação clara do comportamento do INNER JOIN, incluindo a ausência de clientes sem pedidos
046: 
047: ---
048: 
049: ### **8. Cronograma da Aula**
050: 
051: | Tempo | Atividade |
052: |-------|-----------|
053: | 0 – 5 minutos | **Introdução (10 minutos)**: Apresentação do tópico, objetivo da aula, e revisão rápida sobre o que é um JOIN. |
054: | 5 – 15 minutos | **Aprendizagem Direta (20 minutos)**: Explicação do INNER JOIN, com uso de exemplos e demonstração no quadro. |
055: | 15 – 35 minutos | **Atividade em Grupo (20 minutos)**: Os alunos trabalham em grupos para escrever a consulta, determinar o resultado e explicar a ausência de clientes sem pedidos. |
056: | 35 – 45 minutos | **Discussão em Grupo (10 minutos)**: Cada grupo apresenta sua consulta e explica o resultado. |
057: | 45 – 50 minutos | **Conclusão e Avaliação (5 minutos)**: Revisão dos conceitos, resumo da aula, e feedback dos alunos. |
058: 
059: ---
060: 
061: ### **9. Conteúdo Programático**
062: 
063: #### **9.1. Introdução ao INNER JOIN**
064: - Definição: Um tipo de JOIN que retorna apenas as linhas que têm correspondência em ambas as tabelas.
065: - Diferença entre INNER JOIN e outros tipos de JOIN (LEFT JOIN, RIGHT JOIN, FULL JOIN).
066: 
067: #### **9.2. Exemplo Prático**
068: - Tabelas: **clientes** e **pedidos**
069:   - **clientes** = (id_cliente, nome, email)
070:   - **pedidos** = (id_pedido, id_cliente, data_pedido)
071: 
072: #### **9.3. Consulta com INNER JOIN**
073: ```sql
074: SELECT clientes.nome, pedidos.data_pedido
075: FROM clientes
076: INNER JOIN pedidos ON clientes.id_cliente = pedidos.id_cliente;
077: ```
078: 
079: #### **9.4. Análise do Resultado**
080: - A consulta retorna apenas os clientes que têm pedidos.
081: - Clientes que não possuem pedidos não aparecem no resultado, pois não há correspondência na tabela **pedidos**.
082: 
083: ---
084: 
085: ### **10. Avaliação Formativa**
086: - **Produção de consulta SQL correta**  
087: - **Explicação clara do comportamento do INNER JOIN**  
088: - **Listagem de resultados esperados com base na consulta**
089: 
090: ---
091: 
092: ### **11. Recursos Complementares (Opcionais)**
093: - Videoaula curta sobre JOINs (disponível em plataformas como YouTube ou Moodle)  
094: - Exercícios em casa para reforçar o conceito
095: 
096: ---
097: 
098: ### **12. Considerações Finais**
099: A aula busca promover a compreensão prática do INNER JOIN, destacando como ele filtra os dados com base na correspondência entre tabelas. A metodologia colaborativa ajuda os alunos a desenvolver habilidades de comunicação e resolução de problemas, essenciais para a prática de programação.
100: 
101: --- 
102: 
103: **Fim do Plano de Aula**
