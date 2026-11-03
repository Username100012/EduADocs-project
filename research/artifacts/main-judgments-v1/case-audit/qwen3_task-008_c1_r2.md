001: **Plano de Aula: Primeira Forma Normal e Atributos Multivalorados**  
002: **Nível de Ensino:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:**  
007: - Identificar um atributo multivalorado em uma tabela de contatos.  
008: - Reorganizar os dados com valores atômicos.  
009: - Justificar a Primeira Forma Normal (1FN) ao reorganizar os dados.
010: 
011: ---
012: 
013: ## **1. Introdução (5 minutos)**
014: 
015: **Contexto:**  
016: A Primeira Forma Normal (1FN) é um conceito fundamental na teoria de bases de dados relacionais. Ela estabelece que cada célula de uma tabela deve conter apenas um valor atômico (não composto). A violação dessa regra pode levar a inconsistências, problemas de atualização e dificuldades de navegação.
017: 
018: **Objetivo:**  
019: Neste plano, os alunos aprenderão a identificar e reorganizar atributos multivalorados, justificando a aplicação da 1FN.
020: 
021: ---
022: 
023: ## **2. Materiais e Recursos (5 minutos)**
024: 
025: **Materiais:**
026: - **Quadro:** com uma tabela de contatos que inclui múltiplos telefones em uma única célula.
027: - **Folha com tabela de contatos:** com dados de exemplo, incluindo campos como:  
028:   - Nome  
029:   - Endereço  
030:   - Telefone 1  
031:   - Telefone 2  
032:   - Telefone 3  
033: - **Canetas, lápis, marcadores** (para anotações).
034: 
035: **Metodologia:**  
036: - **Resolução colaborativa de problemas:** os alunos trabalharão em grupos para identificar, analisar e resolver o problema.
037: 
038: ---
039: 
040: ## **3. Atividade de Aprendizagem (25 minutos)**
041: 
042: ### **Passo 1: Análise da Tabela de Contatos (5 minutos)**
043: 
044: - Distribuir a tabela de contatos com múltiplos telefones em uma única célula.
045: - Peça aos alunos que observem a tabela e identifiquem os atributos que podem ser considerados multivalorados.
046: 
047: **Exemplo de tabela:**
048: 
049: | Nome    | Endereço         | Telefone |
050: |---------|------------------|----------|
051: | João    | R. Avenida B      | 12345678 90123456 78901234 |
052: 
053: ### **Passo 2: Discussão em Grupo (10 minutos)**
054: 
055: - Perguntas para estimular a reflexão:
056:   - Qual atributo está violando a 1FN?
057:   - Por que o telefone está em uma única célula?
058:   - O que aconteceria se tivessemos que atualizar um número de telefone?
059: 
060: - Os alunos discutem e compartilham suas ideias.
061: 
062: ### **Passo 3: Reorganização da Tabela (10 minutos)**
063: 
064: - Os alunos reorganizam a tabela, separando os telefones em linhas individuais.
065: - Exemplo de tabela reorganizada:
066: 
067: | Nome    | Endereço         | Telefone     |
068: |---------|------------------|--------------|
069: | João    | R. Avenida B      | 12345678     |
070: | João    | R. Avenida B      | 90123456     |
071: | João    | R. Avenida B      | 78901234     |
072: 
073: - Cada telefone é colocado em uma linha separada com o mesmo nome.
074: 
075: ---
076: 
077: ## **4. Explicação e Justificativa (10 minutos)**
078: 
079: - **Explicação da 1FN:**  
080:   Cada célula da tabela deve conter apenas um valor atômico. Quando um atributo contém múltiplos valores, ele é considerado multivalorado, o que viola a 1FN.
081: 
082: - **Justificativa para a reorganização:**  
083:   - Evita inconsistências (ex.: se um telefone for atualizado, precisa ser feito em todas as linhas).
084:   - Facilita a atualização, a inserção e a exclusão de dados.
085:   - Melhora a integridade dos dados e a navegação.
086: 
087: ---
088: 
089: ## **5. Avaliação (5 minutos)**
090: 
091: **Estratégia de Avaliação:**  
092: - **Exposição da tabela reorganizada:** Os alunos apresentam a tabela reorganizada e explicam como os telefones deixaram de ocupar uma única célula.
093: - **Justificativa:** Os alunos justificam a reorganização, relacionando-a à aplicação da 1FN.
094: 
095: **Critérios de Avaliação:**
096: - Identificação correta do atributo multivalorado.
097: - Reorganização correta da tabela.
098: - Explicação clara da aplicação da 1FN.
099: 
100: ---
101: 
102: ## **6. Conclusão e Refletir (5 minutos)**
103: 
104: - **Resumo do conteúdo:**  
105:   - A 1FN exige que cada célula tenha apenas um valor atômico.
106:   - Atributos multivalorados devem ser reorganizados em linhas separadas.
107:   - Isso evita inconsistências e facilita a manipulação de dados.
108: 
109: - **Reflexão:**  
110:   - O que aconteceria se mantivéssemos os telefones em uma única célula?
111:   - Como a 1FN afeta a qualidade dos dados em uma base de dados?
112: 
113: ---
114: 
115: ## **7. Extensão (opcional, 5 minutos)**
116: 
117: - **Exercício extra:**  
118:   - Peça aos alunos a criar uma tabela de contatos com múltiplos e-mails e reorganizá-la, justificando a 1FN.
119:   - Pode ser usado como tarefa de casa ou como atividade de revisão.
120: 
121: ---
122: 
123: ## **Referências (opcional)**
124: 
125: - **Livros:**  
126:   - *Database Systems: The Complete Book* – Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom  
127:   - *Database Management Systems* – Raghu Ramakrishnan, Johannes Gehrke
128: 
129: - **Artigos:**  
130:   - “Understanding the First Normal Form (1NF)” – Oracle University
131: 
132: ---
133: 
134: **Nota:** Este plano de aula pode ser adaptado para diferentes níveis de dificuldade, incluindo a aplicação da 2FN ou 3FN, conforme o progresso dos alunos.
