001: **PLANO DE AULA – Agrupamento SQL com GROUP BY e COUNT**
002: 
003: ---
004: 
005: **Tópico:** Agrupamento SQL com GROUP BY e COUNT  
006: **Nível educacional:** Graduação em Ciência da Computação – Formação introdutória  
007: **Duração:** 50 minutos  
008: **Metodologia:** Resolução colaborativa de problemas  
009: **Materiais e recursos:** Quadro, folha com tabela de pedidos e identificadores de clientes  
010: **Estratégia de avaliação:** Entrega da consulta SQL e justificativa da diferença entre linhas e grupos  
011: 
012: ---
013: 
014: ### **I. Introdução (5 minutos)**
015: 
016: **Objetivo:** Apresentar o conceito de agrupamento em SQL, destacando a utilização de `GROUP BY` e `COUNT` para contar registros por grupo.
017: 
018: - **Contextualização:**  
019:   Introduzir a necessidade de agrupar dados para obtenção de estatísticas, como o número de pedidos por cliente.
020: - **Definições rápidas:**  
021:   - **GROUP BY:** Serve para agrupar linhas com valores iguais em uma coluna.
022:   - **COUNT:** Conta o número de registros em um grupo.
023: - **Exemplo prático:**  
024:   Mostrar um exemplo simples de consulta com `GROUP BY` e `COUNT` para ilustrar o funcionamento.
025: 
026: ---
027: 
028: ### **II. Explicação e Demonstração (10 minutos)**
029: 
030: **Objetivo:** Mostrar como construir uma consulta SQL com `GROUP BY` e `COUNT` para contar pedidos por cliente.
031: 
032: - **Passo 1:**  
033:   Apresentar a tabela de pedidos com as colunas: `id_pedido`, `id_cliente`, `data_pedido`, `valor_pedido`.
034: - **Passo 2:**  
035:   Explicar como utilizar a cláusula `GROUP BY id_cliente` para agrupar os registros por cliente.
036: - **Passo 3:**  
037:   Mostrar a consulta SQL:  
038:   ```sql
039:   SELECT id_cliente, COUNT(*) AS quantidade_pedidos
040:   FROM pedidos
041:   GROUP BY id_cliente;
042:   ```
043: - **Passo 4:**  
044:   Apresentar a saída esperada com o número de pedidos por cliente.
045: 
046: ---
047: 
048: ### **III. Atividade em Grupo (20 minutos)**
049: 
050: **Objetivo:** Os alunos devem escrever a consulta SQL com `GROUP BY` e `COUNT` para contar os pedidos por cliente, com base na tabela fornecida.
051: 
052: - **Instruções:**  
053:   - Os alunos devem trabalhar em grupos de 3 a 4 pessoas.
054:   - Cada grupo recebe uma tabela de pedidos com identificadores de clientes.
055:   - O objetivo é escrever a consulta SQL correta para contar os pedidos por cliente.
056:   - Após a escrita, os grupos devem apresentar a consulta e o resultado esperado.
057: - **Apoio:**  
058:   - O professor fornece a tabela em folha para cada grupo.
059:   - O professor está disponível para orientar os alunos em caso de dúvidas.
060: 
061: ---
062: 
063: ### **IV. Análise e Discussão (10 minutos)**
064: 
065: **Objetivo:** Discutir o resultado da consulta, comparando o número de linhas com o número de grupos.
066: 
067: - **Perguntas para estimular a discussão:**  
068:   - Por que o número de linhas na tabela de pedidos é diferente do número de grupos na consulta?
069:   - Como a cláusula `GROUP BY` afeta a saída da consulta?
070:   - O que aconteceria se tivéssemos clientes com o mesmo `id_cliente`?
071: - **Resposta esperada:**  
072:   - Cada linha na tabela representa um pedido, mas o `GROUP BY` agrupa os registros com o mesmo `id_cliente`, resultando em um grupo por cliente.
073:   - A consulta retorna um registro por cliente, mesmo que ele tenha vários pedidos.
074: 
075: ---
076: 
077: ### **V. Avaliação (5 minutos)**
078: 
079: **Objetivo:** Avaliar a capacidade dos alunos de escrever uma consulta SQL com `GROUP BY` e `COUNT`, e de justificar a diferença entre linhas e grupos.
080: 
081: - **Critérios de avaliação:**  
082:   - Correção da consulta SQL.
083:   - Entendimento da diferença entre linhas na tabela e grupos na consulta.
084:   - Justificativa clara e correta da diferença.
085: - **Forma de avaliação:**  
086:   - Os alunos devem entregar a consulta SQL e a justificativa em folha de papel.
087:   - O professor avalia a precisão e a compreensão do conceito.
088: 
089: ---
090: 
091: ### **VI. Conclusão (5 minutos)**
092: 
093: **Objetivo:** Reforçar o aprendizado e motivar os alunos para a próxima aula.
094: 
095: - **Resumo:**  
096:   - `GROUP BY` é usado para agrupar registros com base em uma coluna.
097:   - `COUNT(*)` conta o número de registros em cada grupo.
098:   - A consulta retorna um registro por grupo, mesmo que haja múltiplos registros na tabela.
099: - **Próxima aula:**  
100:   - Introdução a `HAVING` e `ORDER BY` para filtrar e ordenar resultados de agrupamento.
101: - **Encerramento:**  
102:   - Pergunta motivadora: "Como você usaria essa consulta em um sistema de venda?"  
103:   - Aula encerrada.
104: 
105: ---
106: 
107: **Notas finais:**  
108: - A atividade é colaborativa, favorecendo o debate e a compreensão coletiva.
109: - O uso de uma tabela realista ajuda os alunos a aplicar o conceito em um contexto prático.
110: - A justificativa da diferença entre linhas e grupos é o ponto central da aula, e deve ser bem explorada.
