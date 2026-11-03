001: **Plano de Aula: Primeira Forma Normal e Atributos Multivalorados**
002: 
003: ---
004: 
005: **Tópico:** Primeira Forma Normal e Atributos Multivalorados  
006: **Nível educacional:** Graduação em Ciência da Computação – Formação introdutória  
007: **Duração:** 50 minutos  
008: **Metodologia:** Resolução colaborativa de problemas  
009: **Materiais e recursos:** Quadro, folha com tabela de contatos contendo múltiplos telefones  
010: **Estratégia de avaliação:** Apresentar a tabela reorganizada e explicar como os telefones deixam de ocupar uma única célula multivalorada  
011: 
012: ---
013: 
014: ### **I. Introdução (5 minutos)**
015: 
016: **Objetivo:** Estabelecer o contexto e a importância da Primeira Forma Normal (1FN) no contexto de banco de dados.
017: 
018: - Apresentar a definição de **atributo multivalorado**, destacando que ele contém mais de um valor em uma única célula.
019: - Mostrar a tabela de contatos com múltiplos telefones em uma única coluna.
020: - Introduzir o conceito de **Primeira Forma Normal (1FN)**: uma tabela em que cada célula contém apenas um valor atômico (não pode conter múltiplos valores em uma única célula).
021: - Explicar a justificativa para a normalização, como evitar redundâncias e garantir a integridade dos dados.
022: 
023: ---
024: 
025: ### **II. Atividade de Aprendizagem (30 minutos)**
026: 
027: **Objetivo:** Identificar e reorganizar uma tabela com atributos multivalorados, aplicando a 1FN.
028: 
029: **Passo 1: Análise da tabela (5 minutos)**  
030: - Apresentar a tabela de contatos com os seguintes campos:  
031:   - Nome  
032:   - Email  
033:   - Telefone  
034: - No campo "Telefone", há múltiplos números em uma única célula (ex: "123456789, 987654321").
035: 
036: **Passo 2: Identificação de atributos multivalorados (5 minutos)**  
037: - Com a turma, identificar o atributo "Telefone" como multivalorado.
038: - Discutir as consequências: dados repetidos, dificuldade de atualização, inconsistências.
039: 
040: **Passo 3: Reorganização da tabela (15 minutos)**  
041: - Dividir a turma em grupos para reorganizar a tabela de contatos em conformidade com a 1FN.
042: - Cada grupo deve:
043:   - Criar uma nova tabela com:
044:     - Nome
045:     - Email
046:     - Telefone
047:   - Cada telefone deve estar em uma linha separada.
048:   - Garantir que cada célula contenha apenas um valor atômico.
049: 
050: **Passo 4: Apresentação e Discussão (5 minutos)**  
051: - Cada grupo apresenta sua tabela reorganizada.
052: - Discutir a diferença entre a tabela original e a reorganizada.
053: - Destacar a justificativa para a normalização (eliminação de redundâncias, facilita a atualização, mantém integridade dos dados).
054: 
055: ---
056: 
057: ### **III. Conclusão e Refletir (5 minutos)**
058: 
059: **Objetivo:** Consolidar o conceito de 1FN e reforçar a importância da normalização de dados.
060: 
061: - Resumir os principais pontos:
062:   - Atributo multivalorado: uma célula com mais de um valor.
063:   - 1FN: cada célula contém apenas um valor atômico.
064:   - A normalização ajuda a manter dados consistentes e fáceis de gerenciar.
065: - Perguntas para reflexão:
066:   - Por que é importante não ter múltiplos valores em uma célula?
067:   - Como a normalização ajuda no controle de dados?
068: - Encerrar com uma pergunta para estimular a reflexão:
069:   - "Se você tivesse que armazenar informações de contatos em um banco de dados, como você faria para garantir a integridade dos dados?"
070: 
071: ---
072: 
073: ### **IV. Avaliação**
074: 
075: - **Participação ativa** nas discussões e na reorganização da tabela.
076: - **Apresentação da tabela reorganizada** com valores atômicos em cada célula.
077: - **Explicação clara** do processo de normalização e justificativa para a 1FN.
078: 
079: ---
080: 
081: ### **V. Recursos e Materiais**
082: 
083: - **Quadro:** Para anotar os conceitos e as tabelas.
084: - **Folha com tabela de contatos:** Com múltiplos telefones em uma célula.
085: - **Canetas, lápis, papel:** Para anotações e reorganização da tabela.
086: 
087: ---
088: 
089: ### **VI. Referências (opcional)**
090: 
091: - *Database System Concepts* – Silberschatz, Korth, Sudarshan
092: - *Introdução a Banco de Dados* – Texto didático para graduação
093: 
094: ---
095: 
096: **Fim do plano de aula.**
