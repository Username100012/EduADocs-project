001: **Plano de Aula: Rastreabilidade entre Requisitos e Testes de um Aplicativo de Entregas**
002: 
003: **Nível de Ensino:** Graduação em Ciência da Computação  
004: **Formação:** Introductory (Iniciante)  
005: **Duração:** 50 minutos  
006: **Metodologia:** Resolução colaborativa de problemas  
007: **Objetivo de Aprendizagem:**  
008: - Construir uma matriz relacionando três requisitos de entregas aos testes que os verificam.  
009: - Identificar um requisito sem cobertura.  
010: - Propor um teste para o requisito sem cobertura e justificar a correspondência.
011: 
012: ---
013: 
014: ## **1. Introdução (5 minutos)**
015: 
016: - **Contexto:**  
017:   O aplicativo de entregas precisa garantir que todos os requisitos sejam cobertos por testes. A rastreabilidade entre requisitos e testes é fundamental para garantir a qualidade e a confiabilidade do sistema.
018: 
019: - **Objetivo da aula:**  
020:   Durante a aula, vocês vão trabalhar em grupo para relacionar requisitos de um aplicativo de entregas com os testes correspondentes, identificar um requisito sem cobertura e propor um teste para ele.
021: 
022: ---
023: 
024: ## **2. Materiais e Recursos (5 minutos)**
025: 
026: - **Quadro:** Com os seguintes requisitos:  
027:   1. O usuário deve poder cadastrar um novo entregador.  
028:   2. O sistema deve permitir a atualização de informações do entregador.  
029:   3. O sistema deve exibir uma lista de entregadores cadastrados.
030: 
031: - **Folha com casos de teste:**  
032:   - Caso 1: Cadastrar entregador com nome, CPF e telefone.  
033:   - Caso 2: Atualizar informações de um entregador.  
034:   - Caso 3: Visualizar lista de entregadores.  
035:   - Caso 4: Visualizar lista de entregadores com filtro por cidade.  
036:   - Caso 5: Tentar cadastrar entregador com CPF já existente.
037: 
038: ---
039: 
040: ## **3. Atividade de Resolução Colaborativa (30 minutos)**
041: 
042: ### **Passo 1: Identificar os requisitos (5 minutos)**
043: 
044: - Cada grupo recebe uma folha com os três requisitos e uma lista de casos de teste.
045: - Os alunos devem identificar quais casos de teste correspondem a cada requisito.
046: 
047: ### **Passo 2: Construir a Matriz Requisito-Teste (15 minutos)**
048: 
049: - Os alunos devem criar uma matriz de 3x5, relacionando cada requisito com os testes que o verificam.
050: - Cada aluno deverá preencher a matriz com base na correspondência lógica entre os requisitos e os testes.
051: - O objetivo é identificar se há um requisito que não está coberto por nenhum teste.
052: 
053: ### **Passo 3: Identificar o Requisito Sem Cobertura (5 minutos)**
054: 
055: - Após preencher a matriz, os alunos devem analisar e identificar qual requisito não tem nenhum teste relacionado.
056: - Justificam a identificação, mostrando que o requisito não está coberto.
057: 
058: ### **Passo 4: Propor um Teste para o Requisito Sem Cobertura (5 minutos)**
059: 
060: - Cada grupo propõe um teste que cobre o requisito sem cobertura.
061: - Justificam a correspondência do teste com o requisito, explicando como ele verifica a funcionalidade.
062: 
063: ---
064: 
065: ## **4. Avaliação (5 minutos)**
066: 
067: - **Matriz Requisito-Teste:**  
068:   Os alunos devem entregar a matriz preenchida com os casos de teste associados aos requisitos.
069: 
070: - **Teste Proposto:**  
071:   Cada grupo apresenta o teste que foi proposto para o requisito sem cobertura, justificando sua correspondência.
072: 
073: - **Avaliação:**  
074:   - A matriz deve mostrar uma correspondência lógica entre os requisitos e os testes.  
075:   - O teste proposto deve estar alinhado com o requisito, verificando a funcionalidade de forma adequada.
076: 
077: ---
078: 
079: ## **5. Conclusão (5 minutos)**
080: 
081: - **Resumo da Aula:**  
082:   A rastreabilidade entre requisitos e testes é essencial para garantir que todos os requisitos do sistema sejam cobertos. Através da matriz, podemos identificar requisitos não cobertos e propor testes adequados para eles.
083: 
084: - **Reforço:**  
085:   Os alunos devem entender que a relação entre requisitos e testes é uma prática fundamental no processo de desenvolvimento de software, especialmente em sistemas complexos como aplicativos de entregas.
086: 
087: - **Próxima aula:**  
088:   Trabalhar com diagramas de sequência e testes automatizados.
089: 
090: ---
091: 
092: ## **Matriz Requisito-Teste (Exemplo)**
093: 
094: | Requisito | Caso 1 | Caso 2 | Caso 3 | Caso 4 | Caso 5 |
095: |-----------|--------|--------|--------|--------|--------|
096: | 1. Cadastrar entregador | X | X | X | X | X |
097: | 2. Atualizar informações | X | X | X | X | X |
098: | 3. Exibir lista de entregadores | X | X | X | X | X |
099: 
100: **Requisito sem cobertura:** Nenhum requisito está sem cobertura (neste exemplo).  
101: **Mas, em um cenário real, poderia haver um requisito sem cobertura.**
102: 
103: ---
104: 
105: ## **Teste Proposto para Requisito Sem Cobertura (Exemplo):**
106: 
107: - **Teste:** Verificar se o sistema exibe uma mensagem de erro ao tentar cadastrar um entregador com CPF já existente.  
108: - **Justificativa:** Este teste verifica a funcionalidade de validação de CPF no cadastro de entregador, que está relacionado ao requisito 1.
109: 
110: ---
111: 
112: **Fim do plano de aula.**  
113: Espera-se que os alunos compreendam a importância da rastreabilidade e aprendam a identificar e resolver problemas de cobertura de requisitos.
