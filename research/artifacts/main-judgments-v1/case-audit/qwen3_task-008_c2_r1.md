001: **Plano de Aula: Primeira Forma Normal e Atributos Multivalorados**
002: 
003: ---
004: 
005: ### **Tema:**  
006: **Primeira Forma Normal e Atributos Multivalorados**
007: 
008: ---
009: 
010: ### **Nível Educacional:**  
011: Graduação em Ciência da Computação – Formação Introductory
012: 
013: ---
014: 
015: ### **Duração:**  
016: 50 minutos
017: 
018: ---
019: 
020: ### **Objetivo de Aprendizagem:**  
021: Identificar um atributo multivalorado em uma tabela de contatos e reorganizar os dados com valores atômicos, justificando a Primeira Forma Normal (1FN).
022: 
023: ---
024: 
025: ### **Metodologia:**  
026: Resolução colaborativa de problemas com base em exemplos práticos e discussão em grupo.
027: 
028: ---
029: 
030: ### **Materiais e Recursos:**  
031: - Quadro de branco  
032: - Folha com tabela de contatos contendo múltiplos telefones  
033: - Lápis, caneta e papel para anotações  
034: - Projetor (opcional) para apresentação de exemplos
035: 
036: ---
037: 
038: ### **Conteúdo Programático:**  
039: - Conceito de atributos multivalorados  
040: - Definição da Primeira Forma Normal (1FN)  
041: - Reorganização de dados para atômicos  
042: - Importância da normalização em bancos de dados
043: 
044: ---
045: 
046: ### **Estrutura do Plano de Aula**
047: 
048: #### **1. Introdução (5 minutos)**  
049: - Apresentar o tema de hoje: **Primeira Forma Normal e Atributos Multivalorados**.
050: - Explicar brevemente o que é um atributo multivalorado.
051: - Mostrar uma tabela de contatos com múltiplos telefones em uma única célula.
052: - Perguntar: *"Por que é problemático ter múltiplos números de telefone em uma única célula?"*
053: 
054: ---
055: 
056: #### **2. Explicação Teórica (10 minutos)**  
057: - Definir o conceito de **atributo multivalorado** (ex: múltiplos telefones em uma célula).
058: - Explicar a **Primeira Forma Normal (1FN)**:  
059:   > *"Toda tabela deve ter valores atômicos, ou seja, cada célula deve conter apenas um valor."*
060: - Mostrar a diferença entre uma tabela com atributos multivalorados e uma com valores atômicos.
061: - Exemplo prático:  
062:   - Tabela com telefones em uma célula:  
063:     ```
064:     | Nome     | Telefone         |
065:     |----------|------------------|
066:     | João     | (11) 98765-4321, (11) 98765-4322 |
067:     | Maria    | (11) 98765-4323, (11) 98765-4324 |
068:     ```
069:   - Tabela com valores atômicos:  
070:     ```
071:     | Nome     | Telefone 1     | Telefone 2     |
072:     |----------|----------------|----------------|
073:     | João     | (11) 98765-4321| (11) 98765-4322|
074:     | Maria    | (11) 98765-4323| (11) 98765-4324|
075:     ```
076: 
077: ---
078: 
079: #### **3. Atividade Prática (20 minutos)**  
080: - Distribuir a folha com a tabela de contatos com múltiplos telefones.
081: - Pequenos grupos de 3 a 4 alunos trabalham em conjunto para:
082:   1. Identificar os atributos multivalorados.
083:   2. Reorganizar a tabela com valores atômicos.
084:   3. Explicar o processo de reorganização.
085: - Cada grupo apresenta seu resultado à turma.
086: - Discussão coletiva sobre as justificativas para a normalização.
087: 
088: ---
089: 
090: #### **4. Conclusão e Avaliação (10 minutos)**  
091: - Revisar os pontos principais do dia:
092:   - O que é um atributo multivalorado.
093:   - Por que a 1FN é importante.
094:   - Como reorganizar dados para atômicos.
095: - Avaliação:  
096:   - Observação do desempenho dos alunos na reorganização da tabela.  
097:   - Comentários sobre a explicação dada pelos grupos.
098: - Perguntas de revisão:
099:   - *"Por que não é permitido ter múltiplos valores em uma célula?"*  
100:   - *"Como a 1FN ajuda na manutenção de dados?"*
101: 
102: ---
103: 
104: ### **Recursos Complementares (Opcionais):**  
105: - Videoaula curta sobre normalização de bancos de dados (disponível em plataformas como YouTube ou Coursera).  
106: - Exercícios em PDF para reforço (opcional).
107: 
108: ---
109: 
110: ### **Avaliação Formativa:**  
111: - Participação ativa nas discussões.  
112: - Correção da tabela reorganizada pelos grupos.  
113: - Entendimento do conceito de 1FN e atributos multivalorados.
114: 
115: ---
116: 
117: ### **Próxima Aula (prevista):**  
118: **Segunda Forma Normal (2FN) – Dependência funcional e remoção de atributos redundantes.**
119: 
120: ---
121: 
122: **Fim do Plano de Aula**  
123: *Elaborado com base nos parâmetros pedagógicos fornecidos.*
