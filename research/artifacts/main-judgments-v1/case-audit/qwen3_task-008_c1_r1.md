001: **Plano de Aula: Primeira Forma Normal e Atributos Multivalorados**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:**  
007: Identificar um atributo multivalorado em uma tabela de contatos e reorganizar os dados com valores atômicos, justificando a Primeira Forma Normal (1FN).
008: 
009: ---
010: 
011: ## **1. Introdução (5 minutos)**
012: 
013: **Objetivo:** Introduzir o conceito de Forma Normal e destacar a importância de evitar atributos multivalorados.
014: 
015: - **Definição de Forma Normal 1 (1FN):**  
016:   Uma tabela está na 1FN se cada célula contém apenas um valor atômico (não pode ser dividido em partes menores), e cada linha representa um registro único.
017: 
018: - **Atributo Multivalorado:**  
019:   Um atributo que contém mais de um valor em uma única célula, como "Telefones" em uma tabela de contatos.
020: 
021: - **Motivação:**  
022:   A forma normal ajuda a evitar inconsistências de dados, facilita a manutenção de bancos de dados e assegura a integridade dos dados.
023: 
024: ---
025: 
026: ## **2. Atividade de Introdução (5 minutos)**
027: 
028: **Material:**  
029: - Quadro com uma tabela de contatos (exemplo com múltiplos telefones em uma célula).
030: 
031: **Tarefa:**  
032: - Observar a tabela de contatos e identificar o atributo multivalorado.
033: 
034: **Exemplo de Tabela:**
035: 
036: | Nome      | Endereço         | Telefones             |
037: |-----------|------------------|------------------------|
038: | João      | Rua A, 123       | (11) 98765-4321, (11) 91234-5678 |
039: | Maria     | Rua B, 456       | (21) 98765-4321       |
040: 
041: **Perguntas para reflexão:**  
042: - Qual atributo está com valores multivalorados?  
043: - Por que isso pode causar problemas?
044: 
045: ---
046: 
047: ## **3. Resolução Colaborativa de Problemas (20 minutos)**
048: 
049: **Objetivo:** Reorganizar a tabela de contatos para atender às regras da 1FN.
050: 
051: **Passos:**
052: 
053: 1. **Identificar o atributo multivalorado:**  
054:    - "Telefones" está com múltiplos valores em uma única célula.
055: 
056: 2. **Transformar em atributos individuais:**  
057:    - Criar uma tabela com colunas: `Nome`, `Endereço`, `Telefone1`, `Telefone2`, etc.
058: 
059: 3. **Reorganizar os dados:**  
060:    - Dividir os telefones em linhas separadas.
061: 
062: **Exemplo de Tabela Reorganizada:**
063: 
064: | Nome    | Endereço     | Telefone1       | Telefone2       |
065: |---------|--------------|------------------|------------------|
066: | João    | Rua A, 123   | (11) 98765-4321  | (11) 91234-5678  |
067: | Maria   | Rua B, 456   | (21) 98765-4321  | (null)           |
068: 
069: **Discussão:**  
070: - Por que os telefones não estão mais em uma única célula?  
071: - O que acontece com os dados se mantivermos o atributo multivalorado?  
072: - Qual é a vantagem de ter os dados em valores atômicos?
073: 
074: ---
075: 
076: ## **4. Explicação da 1FN (10 minutos)**
077: 
078: **Objetivo:** Justificar a reorganização dos dados como uma aplicação da 1FN.
079: 
080: - **1FN:**  
081:   Cada célula contém apenas um valor atômico, e cada linha representa um registro único.
082: 
083: - **Benefícios da 1FN:**  
084:   - Evita inconsistências.  
085:   - Facilita a atualização de dados.  
086:   - Melhora a integridade dos dados.  
087:   - Facilita a consulta e a manutenção do banco de dados.
088: 
089: - **Exemplo de problema com atributo multivalorado:**  
090:   - Se um telefone for atualizado, precisa atualizar todos os registros que contêm esse número.
091: 
092: ---
093: 
094: ## **5. Estratégia de Avaliação (10 minutos)**
095: 
096: **Objetivo:** Avaliar a capacidade de identificar e reorganizar atributos multivalorados.
097: 
098: **Atividade:**  
099: - Alunos devem reorganizar uma tabela de contatos fornecida, com múltiplos telefones em uma célula, para seguir a 1FN.
100: 
101: **Critérios de Avaliação:**  
102: - Identificação correta do atributo multivalorado.  
103: - Reorganização correta dos dados em valores atômicos.  
104: - Explicação justificativa da reorganização.
105: 
106: **Formato da Avaliação:**  
107: - Pares de alunos: um responsável por reorganizar, outro por explicar.  
108: - Comentários e feedback entre pares.
109: 
110: ---
111: 
112: ## **6. Conclusão (5 minutos)**
113: 
114: **Resumo do que foi aprendido:**  
115: - Atributos multivalorados devem ser reorganizados para seguir a 1FN.  
116: - A 1FN garante dados atômicos, consistentes e fáceis de manter.  
117: - A reorganização de dados é essencial para a qualidade de um banco de dados.
118: 
119: **Perguntas para reflexão final:**  
120: - Por que é importante seguir a 1FN?  
121: - O que aconteceria se não reorganizássemos os dados?
122: 
123: ---
124: 
125: ## **Materiais e Recursos:**
126: 
127: - Quadro com tabela de contatos com múltiplos telefones em uma célula.
128: - Folha de atividade com a mesma tabela.
129: - Canetas, lápis, papel para anotações.
130: - Possível uso de software de banco de dados (ex.: MySQL, Excel) para ilustração.
131: 
132: ---
133: 
134: ## **Avaliação Formativa:**
135: 
136: - Participação ativa na resolução colaborativa.
137: - Capacidade de identificar e reorganizar atributos multivalorados.
138: - Compreensão e justificação da reorganização.
139: 
140: ---
141: 
142: **Notas Adicionais:**
143: 
144: - Pode-se incluir uma breve introdução ao conceito de dependência funcional e a importância da 1FN no contexto de bancos de dados relacionais.
145: - Recomenda-se a apresentação de uma tabela reorganizada com explicação, como estratégia de avaliação final.
146: 
147: --- 
148: 
149: Espero que esse plano de aula seja útil para a sua prática pedagógica!
