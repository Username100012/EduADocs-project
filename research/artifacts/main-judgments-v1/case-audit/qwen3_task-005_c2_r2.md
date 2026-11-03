001: **Plano de Aula: Chaves Primárias e Estrangeiras em Tabelas de Pedidos**
002: 
003: ---
004: 
005: **Tema:** Chaves primária e estrangeira em tabelas de pedidos  
006: **Nível educacional:** Graduação em Ciência da Computação – Formação introdutória  
007: **Duração:** 50 minutos  
008: **Metodologia:** Resolução colaborativa de problemas  
009: **Materiais e recursos:** Quadro, folha com tabelas de clientes e pedidos  
010: **Estratégia de avaliação:** Marcar as chaves nas duas tabelas e explicar um registro válido e um que viola a integridade referencial
011: 
012: ---
013: 
014: ### **1. Introdução (5 minutos)**
015: 
016: - **Objetivo:** Introduzir os conceitos de chave primária e chave estrangeira, bem como a importância da integridade referencial em bases de dados.
017: - **Aula introdutória:**  
018:   - Apresentar o conceito de tabelas relacionais e a necessidade de relacionar tabelas em um sistema de banco de dados.
019:   - Definir **chave primária** como a chave que identifica de forma única uma linha em uma tabela.
020:   - Definir **chave estrangeira** como uma chave que referencia uma chave primária de outra tabela.
021:   - Apresentar o conceito de **integridade referencial**, que garante que as relações entre tabelas sejam válidas.
022: 
023: ---
024: 
025: ### **2. Atividade de Apresentação (10 minutos)**
026: 
027: - **Objetivo:** Apresentar as tabelas de clientes e pedidos para que os alunos identifiquem as chaves primárias e estrangeiras.
028: - **Material:** Folha com tabelas de clientes e pedidos.
029: - **Conteúdo:**  
030:   - Tabela **clientes** com campos: `cliente_id`, `nome`, `email`.
031:   - Tabela **pedidos** com campos: `pedido_id`, `cliente_id`, `data`, `valor`.
032: - **Perguntas orientadoras:**  
033:   - Qual campo é a chave primária da tabela clientes?  
034:   - Qual campo é a chave primária da tabela pedidos?  
035:   - Qual campo da tabela pedidos é uma chave estrangeira?  
036:   - Por que a chave estrangeira é importante?
037: 
038: ---
039: 
040: ### **3. Atividade de Trabalho em Grupo (20 minutos)**
041: 
042: - **Objetivo:** Identificar as chaves primárias e estrangeiras nas tabelas e verificar a integridade referencial.
043: - **Dividir os alunos em grupos de 3 a 4 pessoas.**
044: - **Distribuir as tabelas de clientes e pedidos.**
045: - **Tarefas para cada grupo:**
046:   - Marcar as chaves primárias nas duas tabelas.
047:   - Marcar as chaves estrangeiras nas duas tabelas.
048:   - Criar dois exemplos de registros:
049:     1. Um registro válido (com integridade referencial).
050:     2. Um registro inválido (que viola a integridade referencial).
051:   - Explicar por que cada registro é válido ou inválido.
052: - **Dica:** Incentivar os alunos a discutir e justificar suas escolhas, especialmente no que diz respeito à integridade referencial.
053: 
054: ---
055: 
056: ### **4. Apresentação dos Resultados (10 minutos)**
057: 
058: - **Objetivo:** Revisar as respostas dos grupos e consolidar o conceito de chaves e integridade referencial.
059: - **Perguntas para a turma:**
060:   - Qual é a chave primária da tabela clientes?  
061:   - Qual é a chave estrangeira da tabela pedidos?  
062:   - Por que a chave estrangeira deve corresponder a uma chave primária existente?
063: - **Revisar os exemplos apresentados pelos grupos:**
064:   - Registros válidos: explicar como eles seguem a regra de integridade.
065:   - Registros inválidos: explicar por que eles não são permitidos.
066: - **Reforçar a importância da integridade referencial** para a consistência e a confiabilidade dos dados no banco de dados.
067: 
068: ---
069: 
070: ### **5. Conclusão e Reforço (5 minutos)**
071: 
072: - **Objetivo:** Consolidar os conceitos e preparar os alunos para aplicar os conhecimentos em atividades práticas.
073: - **Resumo:**
074:   - A **chave primária** identifica de forma única uma linha em uma tabela.
075:   - A **chave estrangeira** estabelece uma relação entre duas tabelas.
076:   - A **integridade referencial** garante que as relações entre tabelas sejam válidas.
077: - **Reflexão final:**
078:   - Por que é importante que as chaves estrangeiras sejam consistentes com as chaves primárias?
079:   - Como isso afeta a qualidade dos dados em um banco de dados?
080: 
081: ---
082: 
083: ### **Avaliação:**
084: 
085: - **Participação ativa nos grupos.**
086: - **Identificação correta das chaves primárias e estrangeiras.**
087: - **Explicação clara de exemplos válidos e inválidos.**
088: 
089: ---
090: 
091: **Nota:** Este plano de aula pode ser adaptado com base no nível de conhecimento dos alunos, incluindo exemplos mais complexos ou introdução a linguagens de consulta (como SQL) para reforçar os conceitos.
