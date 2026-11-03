001: **Plano de Aula: Caso de Uso – Reserva de uma Quadra Esportiva**
002: 
003: **Duração:** 50 minutos  
004: **Nível:** Graduação em Ciência da Computação – Formação Introditória  
005: **Metodologia:** Resolução Colaborativa de Problemas  
006: **Objetivo de Aprendizagem:**  
007: - Descrever ator, pré-condição, fluxo principal e fluxo alternativo de indisponibilidade de uma quadra em um caso de uso de reserva.
008: 
009: ---
010: 
011: ## **I. Introdução (5 minutos)**
012: 
013: **Objetivo:** Apresentar o conceito de caso de uso e sua importância em sistemas de software, com foco em sistemas de reservas de quadras esportivas.
014: 
015: **Conteúdo:**
016: - Definição de caso de uso.
017: - Componentes de um caso de uso: ator, pré-condição, fluxo principal, fluxo alternativo.
018: - Introdução ao sistema de reservas de quadras esportivas como contexto do caso de uso.
019: 
020: **Atividade:**  
021: - Professor apresenta o **Quadro de Caso de Uso** e a **Folha de Descrição do Sistema** (materiais disponíveis).
022: - Alunos respondem a perguntas gerais:
023:   - O que é um caso de uso?
024:   - Por que os fluxos alternativos são importantes?
025: 
026: ---
027: 
028: ## **II. Desenvolvimento (35 minutos)**
029: 
030: ### **Etapa 1: Compartilhamento de Contexto (10 minutos)**
031: 
032: **Material:**  
033: - **Quadro de Caso de Uso** (exemplo de sistema de reservas de quadras)
034: - **Folha de Descrição do Sistema** (com descrição geral do sistema, regras de negócio e fluxos básicos)
035: 
036: **Atividade:**
037: - Professor apresenta o contexto do sistema (ex: sistema de reservas de quadras com data, horário, tipo de quadra, etc.).
038: - Alunos discutem os elementos do sistema e identificam os atores envolvidos (usuário, administrador, sistema, etc.).
039: 
040: ### **Etapa 2: Resolução Colaborativa do Caso de Uso (25 minutos)**
041: 
042: **Objetivo:** Com base no contexto apresentado, os alunos devem criar um caso de uso para **"Reserva de uma Quadra Esportiva"**, com foco em **indisponibilidade da quadra**.
043: 
044: **Passos:**
045: 1. **Definir o ator:**  
046:    - Aluno ou usuário que deseja reservar a quadra.
047: 
048: 2. **Definir a pré-condição:**  
049:    - A quadra deve estar disponível no horário escolhido.
050:    - O usuário deve estar cadastrado no sistema.
051: 
052: 3. **Fluxo principal:**  
053:    - O usuário seleciona a quadra, data e horário.
054:    - O sistema verifica a disponibilidade.
055:    - Se disponível, o sistema confirma a reserva.
056:    - O usuário recebe uma confirmação por e-mail ou SMS.
057: 
058: 4. **Fluxo alternativo (indisponibilidade):**  
059:    - O usuário seleciona a quadra, data e horário.
060:    - O sistema verifica a disponibilidade.
061:    - Se a quadra não estiver disponível, o sistema notifica o usuário.
062:    - O usuário pode escolher outra quadra ou data/horário.
063: 
064: **Apoio:**
065: - Professor orienta a formação de grupos (2-3 alunos por grupo).
066: - Cada grupo recebe o **Quadro de Caso de Uso** e **Folha de Descrição do Sistema**.
067: - Os alunos trabalham colaborativamente para identificar os componentes do caso de uso.
068: 
069: **Discussão:**
070: - O que acontece se a quadra estiver ocupada?
071: - Como o sistema deve reagir a essa condição?
072: - Como justificar a condição que aciona o fluxo alternativo?
073: 
074: ---
075: 
076: ## **III. Avaliação (5 minutos)**
077: 
078: **Objetivo:** Avaliar a compreensão dos alunos sobre os componentes de um caso de uso.
079: 
080: **Atividade:**
081: - Cada grupo apresenta seu caso de uso (ator, pré-condição, fluxo principal e fluxo alternativo).
082: - O professor avalia a **precisão e a coerência** dos fluxos.
083: - **Justificativa da condição do fluxo alternativo:**  
084:   - O fluxo alternativo é acionado quando o sistema detecta que a quadra não está disponível no horário escolhido. Essa condição é estratégica, pois garante que a reserva seja feita apenas em datas e horários disponíveis, evitando conflitos de uso.
085: 
086: ---
087: 
088: ## **IV. Encerramento (5 minutos)**
089: 
090: **Objetivo:** Reforçar o conteúdo e orientar para a próxima aula.
091: 
092: **Conteúdo:**
093: - Resumo dos componentes de um caso de uso.
094: - Importância da resolução colaborativa de problemas.
095: - Aprendizado esperado para a próxima aula (ex: diagrama de sequência).
096: 
097: **Perguntas de Reforço:**
098: - Qual é a função de um fluxo alternativo?
099: - Por que a pré-condição é importante?
100: - Como a condição de indisponibilidade é tratada no sistema?
101: 
102: ---
103: 
104: ## **Recursos Utilizados:**
105: 
106: - **Quadro de Caso de Uso**
107: - **Folha de Descrição do Sistema**
108: - Lápis, caneta, papel
109: 
110: ---
111: 
112: ## **Avaliação do Caso de Uso (Critérios):**
113: 
114: | Critério | Peso | Descrição |
115: |---------|------|-----------|
116: | Identificação do ator | 10% | Correto identificação do ator envolvido. |
117: | Pré-condição | 15% | Correto definição das condições iniciais. |
118: | Fluxo principal | 30% | Correto fluxo de execução do caso de uso. |
119: | Fluxo alternativo | 20% | Correto identificação e justificativa da condição alternativa. |
120: | Coerência e clareza | 25% | Coerência e clareza na descrição do caso de uso. |
121: 
122: ---
123: 
124: **Nota:** Este plano de aula busca promover a **compreensão prática de casos de uso**, com ênfase na **resolução colaborativa** e na **aplicação de conceitos teóricos** em um contexto real.
