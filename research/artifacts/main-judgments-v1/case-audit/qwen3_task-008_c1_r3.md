001: **Plano de Aula: Primeira Forma Normal e Atributos Multivalorados**  
002: **Nível de Ensino:** Graduação em Ciência da Computação  
003: **Formação:** Introdutória  
004: **Duração:** 50 minutos  
005: **Objetivo de Aprendizagem:**  
006: Identificar um atributo multivalorado em uma tabela de contatos e reorganizar os dados com valores atômicos, justificando a Primeira Forma Normal (1FN).
007: 
008: ---
009: 
010: ### **1. Introdução (5 minutos)**
011: 
012: **Objetivo:** Introduzir o conceito de atributos multivalorados e a necessidade da Primeira Forma Normal (1FN).
013: 
014: - **Perguntas de motivação:**
015:   - Por que é importante ter dados "puros" em uma tabela?
016:   - O que acontece se um atributo tiver mais de um valor em uma única célula?
017: - **Definições rápidas:**
018:   - Atributo multivalorado: um atributo que contém mais de um valor em uma única célula.
019:   - Primeira Forma Normal (1FN): uma forma normal em que cada célula contém apenas um valor atômico (não dividido, não agrupado).
020: - **Contexto:** Apresentar a tabela de contatos com múltiplos telefones como exemplo de atributo multivalorado.
021: 
022: ---
023: 
024: ### **2. Atividade Introdutória: Análise da Tabela de Contatos (10 minutos)**
025: 
026: **Materiais:**
027: - Quadro com tabela de contatos com múltiplos telefones (exemplo: nome, endereço, telefones).
028: - Folha com a mesma tabela para os alunos.
029: 
030: **Descrição:**
031: - **Passo 1:** Mostrar a tabela de contatos com um atributo "telefones" que contém múltiplos números em uma única célula.
032: - **Passo 2:** Pedir aos alunos que identifiquem o atributo multivalorado e discutam por que isso pode ser problemático.
033: - **Passo 3:** Iniciar uma discussão sobre a necessidade de separar os telefones em linhas distintas.
034: 
035: ---
036: 
037: ### **3. Resolução Colaborativa de Problemas (20 minutos)**
038: 
039: **Objetivo:** Reorganizar a tabela de contatos em conformidade com a 1FN.
040: 
041: **Passos:**
042: 
043: 1. **Identificar o problema:**
044:    - Atributo "telefones" é multivalorado.
045:    - Cada linha de contato tem múltiplos números em uma célula.
046: 
047: 2. **Reorganizar os dados:**
048:    - Criar uma nova tabela com colunas: `id_contato`, `nome`, `endereco`, `telefone`.
049:    - Cada número de telefone será uma linha separada.
050:    - Exemplo:
051:      ```
052:      id_contato | nome     | endereco       | telefone
053:      1          | João     | R. Avenida 100  | 123456789
054:      1          | João     | R. Avenida 100  | 987654321
055:      ```
056: 
057: 3. **Discussão:**
058:    - Por que é importante ter cada telefone em uma linha separada?
059:    - Como isso ajuda a manter a integridade dos dados?
060:    - Como isso evita problemas de inconsistência?
061: 
062: 4. **Justificar a 1FN:**
063:    - Cada célula contém apenas um valor atômico.
064:    - Cada linha representa uma entidade (um contato).
065:    - Não há atributos compostos ou agrupados.
066: 
067: ---
068: 
069: ### **4. Avaliação (10 minutos)**
070: 
071: **Estratégia:** Apresentar a tabela reorganizada e explicar como os telefones deixam de ocupar uma única célula multivalorada.
072: 
073: - **Perguntas de avaliação:**
074:   - O que você entende por atributo multivalorado?
075:   - Por que a 1FN é importante?
076:   - Como a tabela reorganizada ajuda a manter a integridade dos dados?
077: 
078: - **Resposta esperada:**
079:   - Atributo multivalorado é um atributo que contém mais de um valor em uma única célula.
080:   - A 1FN é importante porque garante que cada célula contenha apenas um valor atômico, evitando inconsistências e facilitando a manipulação dos dados.
081:   - A reorganização separa os telefones em linhas distintas, evitando que um único atributo contenha múltiplos valores.
082: 
083: ---
084: 
085: ### **5. Conclusão (5 minutos)**
086: 
087: - **Resumo:**
088:   - Atributos multivalorados são problemáticos e devem ser reorganizados para seguir a 1FN.
089:   - A reorganização dos dados em linhas separadas garante que cada célula contenha apenas um valor atômico.
090: - **Reforço:**
091:   - A 1FN é o primeiro passo para normalizar uma tabela.
092:   - A normalização ajuda a manter dados consistentes e fáceis de manipular.
093: 
094: ---
095: 
096: ### **Recursos Utilizados:**
097: - Quadro com tabela de contatos com múltiplos telefones.
098: - Folha com a mesma tabela para os alunos.
099: - Projetor ou pizarrão para apresentação de exemplos.
100: 
101: ---
102: 
103: ### **Apoio para Aprendizagem:**
104: - Para alunos com dificuldades, fornecer uma tabela simplificada com apenas um telefone por linha.
105: - Para alunos mais avançados, apresentar exemplos de tabelas com múltiplos atributos multivalorados e como reorganizá-los.
106: 
107: ---
108: 
109: ### **Duração Total:** 50 minutos  
110: **Metodologia:** Resolução colaborativa de problemas  
111: **Estratégia de Avaliação:** Apresentação da tabela reorganizada e explicação do processo.
