001: **Plano de Aula: INNER JOIN entre Clientes e Pedidos**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Objetivo de Aprendizagem:**  
006: - Escrever uma consulta SQL com INNER JOIN entre as tabelas *clientes* e *pedidos*.  
007: - Determinar as linhas retornadas quando um cliente **não possui** pedidos.  
008: - Compreender a diferença entre INNER JOIN e outros tipos de JOIN (como LEFT JOIN).  
009: - Aplicar a metodologia de **resolução colaborativa de problemas** para desenvolver a consulta.  
010: 
011: ---
012: 
013: ### **1. Introdução (5 minutos)**  
014: **Objetivo:** Contextualizar o conceito de JOIN e apresentar a tarefa.  
015: 
016: - **Professor:**  
017:   - Introduzir o conceito de JOIN como operador de combinação de tabelas.  
018:   - Explicar o que é um **INNER JOIN** e como ele retorna apenas as linhas com registros correspondentes nas duas tabelas.  
019:   - Apresentar as duas tabelas: *clientes* e *pedidos*, com exemplos de dados.  
020:   - Explicar o objetivo da aula: escrever uma consulta INNER JOIN e determinar quais clientes têm pedidos.  
021:   - **Pergunta inicial:** "Qual é a diferença entre INNER JOIN e LEFT JOIN?"  
022:   - Distribuir **quadro de dados** (com as tabelas *clientes* e *pedidos*) e **folha de atividade** para os alunos.  
023: 
024: ---
025: 
026: ### **2. Atividade Colaborativa (25 minutos)**  
027: **Objetivo:** Os alunos trabalham em grupos para criar a consulta SQL e analisar os resultados.  
028: 
029: **Materiais:**  
030: - Quadro com as tabelas *clientes* e *pedidos* (com dados fictícios, como a seguir):  
031:   **Tabela clientes:**  
032:   | ID_Cliente | Nome         | Email               |  
033:   |------------|--------------|---------------------|  
034:   | 1          | João Silva   | joao@example.com   |  
035:   | 2          | Maria Oliveira | maria@example.com |  
036:   | 3          | Carlos Souza | carlos@example.com |  
037:   | 4          | Ana Souza    | ana@example.com    |  
038: 
039:   **Tabela pedidos:**  
040:   | ID_Pedido | ID_Cliente | Data_pedido | Valor |  
041:   |-----------|------------|-------------|-------|  
042:   | 101       | 1          | 2023-01-01  | 100   |  
043:   | 102       | 2          | 2023-01-02  | 150   |  
044:   | 103       | 1          | 2023-01-03  | 200   |  
045: 
046: **Passos da Atividade:**  
047: 1. **Grupo 1:** Escrever a consulta SQL com INNER JOIN entre *clientes* e *pedidos*.  
048: 2. **Grupo 2:** Executar a consulta e listar os resultados.  
049: 3. **Grupo 3:** Explicar por que alguns clientes não aparecem na consulta.  
050: 4. **Grupo 4:** Comparar com um LEFT JOIN e discutir a diferença.  
051: 
052: **Instruções para os alunos:**  
053: - Usar o quadro para identificar os registros correspondentes.  
054: - Escrever a consulta SQL no quadro.  
055: - Comentar sobre os resultados obtidos.  
056: - Discutir a ausência de clientes que não possuem pedidos.  
057: 
058: ---
059: 
060: ### **3. Explicação e Discussão (10 minutos)**  
061: **Objetivo:** Clarificar a diferença entre INNER JOIN e LEFT JOIN e a ausência de clientes sem pedidos.  
062: 
063: - **Professor:**  
064:   - Explicar que o INNER JOIN retorna apenas os clientes que possuem pelo menos um pedido.  
065:   - Mostrar que clientes sem pedidos não são incluídos na consulta.  
066:   - Comparar com um LEFT JOIN, que inclui todos os clientes, mesmo sem pedidos.  
067:   - **Pergunta final:** "Por que os clientes sem pedidos não aparecem na consulta?"  
068:   - Discutir a estratégia de avaliação: os alunos devem identificar que clientes não possuem pedidos e explicar por que não aparecem no resultado.  
069: 
070: ---
071: 
072: ### **4. Avaliação (5 minutos)**  
073: **Objetivo:** Verificar o entendimento do conceito e a aplicação da consulta.  
074: 
075: - **Professor:**  
076:   - Distribuir uma **folha de avaliação** com perguntas como:  
077:     - Qual é a consulta SQL correta para um INNER JOIN?  
078:     - Por que os clientes sem pedidos não aparecem na consulta?  
079:     - Diferencie INNER JOIN de LEFT JOIN.  
080:   - Os alunos respondem individualmente, com base no que estudaram.  
081: 
082: ---
083: 
084: ### **5. Encerramento e Refletir (5 minutos)**  
085: **Objetivo:** Concluir a aula e reforçar o conteúdo.  
086: 
087: - **Professor:**  
088:   - Resumir os pontos principais:  
089:     - INNER JOIN retorna apenas os clientes com pedidos.  
090:     - Clientes sem pedidos não aparecem na consulta.  
091:     - A metodologia colaborativa ajuda a compreender melhor os conceitos.  
092:   - Perguntar: "O que você aprendeu hoje?"  
093:   - Avisar sobre a próxima aula (LEFT JOIN e outras operações).  
094: 
095: ---
096: 
097: ### **Material Adicional (Disponível para os Alunos):**  
098: - Tabelas *clientes* e *pedidos*  
099: - Folha de atividade com consulta SQL  
100: - Folha de avaliação (opcional)  
101: 
102: ---
103: 
104: **Notas Finais:**  
105: - Esta aula combina teoria, prática e colaboração, permitindo que os alunos compreendam melhor o conceito de JOIN.  
106: - O uso de tabelas pequenas facilita a compreensão e a aplicação prática.  
107: - A estratégia de avaliação está baseada na identificação de clientes sem pedidos, que é um ponto essencial do INNER JOIN.
