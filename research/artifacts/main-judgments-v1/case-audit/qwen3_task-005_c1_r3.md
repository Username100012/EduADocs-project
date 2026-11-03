001: **Plano de Aula: Chaves Primárias e Estrangeiras nas Tabelas de Pedidos**
002: 
003: ---
004: 
005: **Disciplina:** Bases de Dados  
006: **Nível:** Graduação em Ciência da Computação  
007: **Formação:** Introdutória  
008: **Duração:** 50 minutos  
009: **Objetivo de Aprendizagem:**  
010: - Identificar chaves primárias e estrangeiras nas tabelas *clientes* e *pedidos*.  
011: - Justificar a integridade referencial em dois exemplos.  
012: 
013: ---
014: 
015: ### **1. Introdução (5 minutos)**
016: 
017: **Objetivo:** Contextualizar o conceito de chaves primárias e estrangeiras e sua importância na integridade referencial.
018: 
019: - Explicar brevemente o conceito de **chave primária** (única e não nula) e **chave estrangeira** (link entre tabelas).
020: - Apresentar o exemplo de uma base de dados com tabelas *clientes* e *pedidos*.
021: - Destacar a importância da integridade referencial para manter a coerência dos dados.
022: 
023: ---
024: 
025: ### **2. Atividade de Introdução (10 minutos)**
026: 
027: **Materiais:**  
028: - Quadro com tabelas *clientes* e *pedidos* (exemplos de registros).  
029: - Folha de papel com as mesmas tabelas (para os alunos marcarem as chaves).  
030: - Lápis, caneta, marcador.  
031: 
032: **Descrição da Atividade:**  
033: - Os alunos trabalham em grupos de 2–3 pessoas.  
034: - Cada grupo recebe as tabelas *clientes* e *pedidos* com alguns registros.  
035: - Os alunos devem identificar a **chave primária** e a **chave estrangeira** em cada tabela.  
036: - Marcar as chaves nas tabelas com marcadores (ou escrever as chaves no quadro).  
037: - Discutir como as tabelas estão relacionadas (chave estrangeira de *pedidos* é a *id_cliente* da tabela *clientes*).
038: 
039: ---
040: 
041: ### **3. Resolução Colaborativa de Problemas (20 minutos)**
042: 
043: **Objetivo:** Aplicar o conceito de chaves primárias e estrangeiras em exemplos reais.
044: 
045: **Passo a Passo:**
046: 
047: 1. **Exemplo 1: Registro Válido**  
048:    - Mostrar um registro válido de *pedidos* com uma chave estrangeira que existe na tabela *clientes*.  
049:    - Os alunos identificam que o registro está correto e justificam por que é válido (a chave estrangeira existe na tabela *clientes*).
050: 
051: 2. **Exemplo 2: Registro Inválido**  
052:    - Mostrar um registro de *pedidos* com uma chave estrangeira que **não existe** na tabela *clientes*.  
053:    - Os alunos identificam que o registro viola a integridade referencial e explicam por que isso é um problema (o cliente não existe, então o pedido não pode existir).
054: 
055: 3. **Discussão em Grupo:**  
056:    - Cada grupo apresenta seus exemplos e justifica a validade ou a violação da integridade referencial.  
057:    - O professor orienta e corrigem eventuais erros.
058: 
059: ---
060: 
061: ### **4. Avaliação (10 minutos)**
062: 
063: **Estratégia de Avaliação:**  
064: - Os alunos marcam as chaves primárias e estrangeiras nas tabelas fornecidas.  
065: - Cada grupo apresenta um registro válido e um inválido, explicando por que cada um é válido ou inválido.  
066: - O professor verifica se os alunos identificaram corretamente as chaves e justificam adequadamente a integridade referencial.
067: 
068: ---
069: 
070: ### **5. Conclusão (5 minutos)**
071: 
072: **Resumo:**  
073: - Reforçar o conceito de chaves primárias e estrangeiras.  
074: - Destacar a importância da integridade referencial para a consistência dos dados.  
075: - Incentivar a aplicação desses conceitos em projetos de banco de dados futuros.
076: 
077: **Perguntas de Refletência:**  
078: - Por que a integridade referencial é importante em sistemas de gestão?  
079: - Como você aplicaria esse conceito em um projeto de sistema de venda?
080: 
081: ---
082: 
083: ### **Materiais e Recursos:**
084: 
085: - Quadro com tabelas *clientes* e *pedidos* (com exemplos de registros).  
086: - Folha de papel com as mesmas tabelas para os alunos.  
087: - Lápis, marcador, caneta.  
088: - Pincel e quadro para marcar as chaves.
089: 
090: ---
091: 
092: ### **Duração Total do Plano de Aula: 50 minutos**
093: 
094: ---
095: 
096: **Nota:** Este plano de aula foi elaborado com base na metodologia de **resolução colaborativa de problemas**, promovendo a interação entre os alunos e a aplicação prática dos conceitos teóricos.
