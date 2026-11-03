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
017:   - Explicar brevemente o que é um *JOIN* em SQL e sua importância para combinar dados de tabelas relacionadas.  
018:   - Apresentar as duas tabelas: *clientes* e *pedidos*.  
019:   - Dizer que a tarefa é:  
020:     - Escrever uma consulta SQL com *INNER JOIN* entre as tabelas *clientes* e *pedidos*.  
021:     - Determinar quais linhas serão retornadas, especialmente quando um cliente **não** tem pedidos.  
022:   - Dizer que os alunos farão isso em grupo, usando o quadro e as tabelas fornecidas.  
023: 
024: ---
025: 
026: ### **2. Recursos Disponíveis (2 minutos)**  
027: **Objetivo:** Familiarizar os alunos com os recursos que estarão disponíveis.  
028: 
029: - **Quadro de whiteboard:** Para anotar a consulta SQL e o resultado esperado.  
030: - **Tabelas pequenas:**  
031:   - *Clientes*:  
032:     | ID_Cliente | Nome         |  
033:     |------------|--------------|  
034:     | 1          | João         |  
035:     | 2          | Maria        |  
036:     | 3          | Carlos       |  
037:     | 4          | Ana          |  
038: 
039:   - *Pedidos*:  
040:     | ID_Pedido | ID_Cliente | Data           |  
041:     |-----------|------------|----------------|  
042:     | 101       | 1          | 2023-04-01     |  
043:     | 102       | 2          | 2023-04-02     |  
044:     | 103       | 3          | 2  
045:     | 104       | 4          | 2023-04-04     |  
046: 
047: - **Dica:** O aluno com ID 3 (Carlos) **não** tem pedidos na tabela *pedidos*.  
048: 
049: ---
050: 
051: ### **3. Resolução Colaborativa (25 minutos)**  
052: 
053: **Etapa 1: Compreender as tabelas (5 minutos)**  
054: - Os alunos analisam as tabelas e identificam as chaves primárias e a relação entre as tabelas.  
055: - Identificam que *ID_Cliente* é a chave primária da tabela *clientes* e uma chave estrangeira na tabela *pedidos*.  
056: 
057: **Etapa 2: Escrever a consulta INNER JOIN (10 minutos)**  
058: - Os alunos trabalham em grupo para escrever a consulta SQL:  
059:   ```sql
060:   SELECT clientes.ID_Cliente, clientes.Nome, pedidos.ID_Pedido
061:   FROM clientes
062:   INNER JOIN pedidos ON clientes.ID_Cliente = pedidos.ID_Cliente;
063:   ```  
064: - O professor circula para ajudar e corrigir dúvidas.  
065: 
066: **Etapa 3: Analisar o resultado (5 minutos)**  
067: - O grupo executa a consulta e analisa o resultado.  
068: - Identificam que **Carlos (ID 3)** não aparece no resultado, pois não tem pedidos.  
069: 
070: **Etapa 4: Comparar com LEFT JOIN (5 minutos)**  
071: - O professor apresenta uma consulta *LEFT JOIN*:  
072:   ```sql
073:   SELECT clientes.ID_Cliente, clientes.Nome, pedidos.ID_Pedido
074:   FROM clientes
075:   LEFT JOIN pedidos ON clientes.ID_Cliente = pedidos.ID_Cliente;
076:   ```  
077: - Os alunos observam que, com *LEFT JOIN*, todos os clientes aparecem, mesmo que não tenham pedidos.  
078: 
079: ---
080: 
081: ### **4. Explicação da Estratégia de Avaliação (5 minutos)**  
082: **Objetivo:** Avaliar a compreensão do aluno sobre o funcionamento do INNER JOIN.  
083: 
084: - O professor explica que, no INNER JOIN, **apenas os clientes com pedidos** são retornados.  
085: - O cliente sem pedidos (Carlos) **não aparece** no resultado, pois o INNER JOIN ignora as linhas que não têm correspondência na outra tabela.  
086: - A tarefa de identificar esse comportamento é uma estratégia de avaliação.  
087: 
088: ---
089: 
090: ### **5. Conclusão e Reflexão (3 minutos)**  
091: **Objetivo:** Reforçar o conteúdo e preparar para a próxima aula.  
092: 
093: - **Professor:**  
094:   - Resuma o que foi aprendido: o INNER JOIN retorna apenas os registros que têm correspondência nas duas tabelas.  
095:   - Destaque a importância de escolher o tipo de JOIN correto dependendo do objetivo.  
096:   - Pergunte: *Qual é a diferença entre INNER JOIN e LEFT JOIN?*  
097:   - Diga que a próxima aula trará o tema de LEFT JOIN e RIGHT JOIN.  
098: 
099: ---
100: 
101: ### **Avaliação Formativa**  
102: - **Participação ativa no grupo de resolução colaborativa.**  
103: - **Capacidade de escrever corretamente a consulta INNER JOIN.**  
104: - **Capacidade de identificar a ausência do cliente sem pedidos.**  
105: 
106: ---
107: 
108: ### **Recursos Adicionais (opcional)**  
109: - Exemplo de consulta com INNER JOIN no banco de dados real (se disponível).  
110: - Exercícios complementares com outras tabelas.  
111: 
112: ---
113: 
114: **Fim do Plano de Aula**  
115: **Duração total: 50 minutos**  
116: **Metodologia:** Resolução colaborativa de problemas  
117: **Habilidades desenvolvidas:** Uso de SQL, compreensão de JOINs, análise de dados e trabalho em grupo.
