001: **Plano de Aula: Chaves Primárias e Estrangeiras nas Tabelas de Clientes e Pedidos**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação  
005: **Formação:** Introdutória  
006: **Metodologia:** Resolução colaborativa de problemas  
007: **Conteúdo:** Chaves primárias, chaves estrangeiras, integridade referencial  
008: **Recursos:** Quadro de whiteboard, folha com tabelas de clientes e pedidos, canetas, lápis
009: 
010: ---
011: 
012: ## **Objetivo de Aprendizagem:**
013: 
014: - Identificar chaves primárias e chaves estrangeiras nas tabelas de clientes e pedidos.
015: - Justificar a importância da integridade referencial em dois exemplos práticos.
016: 
017: ---
018: 
019: ## **Estrutura do Plano de Aula:**
020: 
021: ### **1. Introdução (5 minutos)**
022: 
023: **Objetivo:** Contextualizar o conceito de chaves primárias e estrangeiras e a importância da integridade referencial.
024: 
025: - Apresentar a ideia de **chave primária** como um identificador único de uma entidade (como um CPF ou ID de cliente).
026: - Apresentar a **chave estrangeira** como uma referência a outra tabela (como o ID do cliente em uma tabela de pedidos).
027: - Introduzir o conceito de **integridade referencial**, que garante que os dados sejam consistentes e não existam registros inválidos (ex.: um pedido com um cliente que não existe).
028: 
029: **Duração:** 5 minutos
030: 
031: ---
032: 
033: ### **2. Atividade de Apresentação (10 minutos)**
034: 
035: **Objetivo:** Mostrar as tabelas de clientes e pedidos com dados de exemplo.
036: 
037: - **Tabela de Clientes:**
038:   | ID_Cliente | Nome         | Endereço        | Telefone         |
039:   |------------|--------------|-----------------|------------------|
040:   | 1          | João Silva   | R. Avenida B     | (11) 98765-4321 |
041:   | 2          | Maria Oliveira | R. Rua C        | (11) 98765-4322 |
042:   | 3          | Carlos Souza | R. Estrada D    | (11) 98765-4323 |
043: 
044: - **Tabela de Pedidos:**
045:   | ID_Pedido | ID_Cliente | Data         | Valor      |
046:   |-----------|------------|--------------|------------|
047:   | 101       | 1          | 2024-04-05   | 150.00     |
048:   | 102       | 2          | 2024-04-06   | 200.00     |
049:   | 103       | 4          | 2024-04-07   | 80.00      |
050: 
051: **Duração:** 10 minutos
052: 
053: ---
054: 
055: ### **3. Atividade Colaborativa: Identificação de Chaves (15 minutos)**
056: 
057: **Objetivo:** Identificar e marcar as chaves primárias e estrangeiras nas tabelas.
058: 
059: - **Instruções:**
060:   - Dividir a turma em grupos de 3 a 4 alunos.
061:   - Cada grupo recebe uma folha com as tabelas de clientes e pedidos.
062:   - Os alunos devem marcar as chaves primárias e estrangeiras.
063:   - Explicar por que cada campo é uma chave primária ou estrangeira.
064: 
065: **Estratégia de Avaliação:**
066: - Cada grupo apresenta suas conclusões.
067: - O professor verifica e corrigem as respostas.
068: 
069: **Duração:** 15 minutos
070: 
071: ---
072: 
073: ### **4. Atividade de Discussão: Integridade Referencial (10 minutos)**
074: 
075: **Objetivo:** Analisar dois exemplos de registros, um válido e outro que viola a integridade referencial.
076: 
077: **Exemplo 1 (Válido):**
078: - ID_Pedido = 101, ID_Cliente = 1 → Cliente existe na tabela de clientes.
079: 
080: **Exemplo 2 (Inválido):**
081: - ID_Pedido = 103, ID_Cliente = 4 → Cliente 4 não existe na tabela de clientes.
082: 
083: **Discussão:**
084: - Por que o segundo exemplo é inválido?
085: - O que acontece se um pedido for inserido com um ID de cliente que não existe?
086: - Como manter a integridade referencial?
087: 
088: **Duração:** 10 minutos
089: 
090: ---
091: 
092: ### **5. Conclusão e Refletir (10 minutos)**
093: 
094: **Objetivo:** Sintetizar o conteúdo e reforçar o entendimento.
095: 
096: - Resumir os conceitos de chave primária, chave estrangeira e integridade referencial.
097: - Refletir sobre a importância de manter a coerência entre tabelas.
098: - Perguntas de reflexão:
099:   - Por que a integridade referencial é importante em sistemas de banco de dados?
100:   - Como você aplicaria esses conceitos em um projeto real?
101: 
102: **Duração:** 10 minutos
103: 
104: ---
105: 
106: ## **Avaliação:**
107: 
108: - **Participação ativa nos grupos.**
109: - **Identificação correta das chaves primárias e estrangeiras.**
110: - **Explicação clara do exemplo de integridade referencial.**
111: 
112: ---
113: 
114: ## **Recursos Utilizados:**
115: 
116: - Quadro de whiteboard
117: - Folha com tabelas de clientes e pedidos
118: - Canetas, lápis
119: - Perguntas e exemplos de registros
120: 
121: ---
122: 
123: ## **Nota Final:**
124: 
125: Este plano de aula busca promover uma compreensão prática e colaborativa dos conceitos de chaves primárias e estrangeiras, além de reforçar a importância da integridade referencial em sistemas de banco de dados. A abordagem prática com tabelas e exemplos ajuda a consolidar o aprendizado.
