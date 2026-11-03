001: **Plano de Aula: Particionamento de Equivalência para Validação de Idade**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introductory  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:**  
007: - Identificar partições válidas e inválidas para um campo que aceita idades inteiras de zero a 120.  
008: - Selecionar entradas de teste representativas para validar o comportamento do sistema.  
009: 
010: ---
011: 
012: ## **1. Introdução (5 minutos)**
013: 
014: **Objetivo:** Introduzir o conceito de *particionamento de equivalência* e sua aplicação na validação de dados.  
015: - Definir o conceito de *particionamento de equivalência* como uma técnica de teste que divide o domínio de valores em classes equivalentes, onde as entradas de uma classe são esperadas comportar-se de forma semelhante.  
016: - Apresentar o problema: validar um campo de entrada de idade que aceita valores inteiros entre 0 e 120.  
017: - Explicar que o objetivo é identificar quais valores são *válidos* e quais são *inválidos* e escolher entradas de teste para cobrir essas classes.  
018: 
019: **Material:**  
020: - Quadro de whiteboard  
021: - Folha com a especificação de validação:  
022:   > "O campo de idade deve aceitar valores inteiros entre 0 e 120. Valores fora desse intervalo são considerados inválidos."
023: 
024: ---
025: 
026: ## **2. Atividade de Resolução Colaborativa (30 minutos)**
027: 
028: **Objetivo:** Dividir o intervalo de 0 a 120 em classes equivalentes, identificar as partições válidas e inválidas, e selecionar entradas de teste representativas.  
029: 
030: **Passos da Atividade:**  
031: 1. **Divisão do domínio em classes:**  
032:    - A turma divide-se em grupos de 3–4 alunos.  
033:    - Cada grupo deve identificar as classes equivalentes para o campo de idade.  
034:    - Exemplo de classes:  
035:      - Classe válida: 0 a 120 (inclusive)  
036:      - Classe inválida: menores que 0  
037:      - Classe inválida: maiores que 120  
038: 
039: 2. **Identificação de entradas de teste:**  
040:    - Cada grupo deve escolher 3 entradas de teste que representem as classes identificadas.  
041:    - Exemplo de entradas:  
042:      - Válida: 25  
043:      - Inválida: -5  
044:      - Inválida: 130  
045: 
046: 3. **Classificação das entradas:**  
047:    - Cada grupo apresenta suas entradas de teste e classifica-as como válidas ou inválidas.  
048:    - O professor verifica as respostas corretas e fornece feedback.  
049: 
050: 4. **Discussão coletiva:**  
051:    - Todos os grupos compartilham suas partições e entradas.  
052:    - O professor destaca as melhores práticas e corrigem possíveis erros.  
053: 
054: ---
055: 
056: ## **3. Avaliação (10 minutos)**
057: 
058: **Objetivo:** Avaliar a capacidade dos alunos de identificar classes equivalentes e escolher entradas de teste representativas.  
059: 
060: **Estratégia de Avaliação:**  
061: - **Classificação das Partições:**  
062:   - Válidas: 0 a 120  
063:   - Inválidas: menores que 0 ou maiores que 120  
064: 
065: - **Entradas de Teste:**  
066:   - 3 entradas: 1 entrada válida e 2 entradas inválidas  
067:   - Exemplo:  
068:     - Entrada 1: 25 (válida)  
069:     - Entrada 2: -5 (inválida)  
070:     - Entrada 3: 130 (inválida)  
071: 
072: **Resultado Esperado:**  
073: - Os alunos devem identificar as partições corretas e selecionar entradas que cobrem as classes válidas e inválidas.  
074: 
075: ---
076: 
077: ## **4. Conclusão e Reflexão (5 minutos)**
078: 
079: **Objetivo:** Refletir sobre o processo de particionamento e sua importância na prática de testes automatizados e manuais.  
080: 
081: - Perguntas para reflexão:  
082:   - Por que é importante dividir o domínio de valores em classes?  
083:   - Como a escolha de entradas de teste afeta a eficiência do teste?  
084:   - Qual a vantagem de testar classes equivalentes em vez de cada valor individualmente?  
085: 
086: **Feedback do Professor:**  
087: - Destaca os pontos fortes da atividade e sugere ações para aprimorar o entendimento.  
088: - Oferece sugestões para aprofundamento, como testes de borda ou testes de equivalência com múltiplas condições.  
089: 
090: ---
091: 
092: ## **Materiais e Recursos Utilizados:**
093: 
094: - **Quadro:** Para anotar as partições e as entradas de teste.  
095: - **Folha:** Com a especificação de validação do campo de idade.  
096: - **Papel e caneta:** Para anotações individuais.  
097: 
098: ---
099: 
100: ## **Avaliação Formativa (Pré-Requisito):**  
101: - Conhecimento básico de testes de software, especialmente de testes de equivalência.  
102: - Familiaridade com conceitos de validação de entradas.  
103: 
104: ---
105: 
106: **Nota:** Este plano de aula pode ser adaptado para incluir exemplos de código ou ferramentas de testes automatizados, se for necessário.
