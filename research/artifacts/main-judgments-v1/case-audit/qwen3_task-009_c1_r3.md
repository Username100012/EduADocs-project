001: **Plano de Aula: Caso de Uso – Reserva de uma Quadra Esportiva**
002: 
003: ---
004: 
005: **Nível de Ensino:** Graduação em Ciência da Computação  
006: **Carga Horária:** 50 minutos  
007: **Metodologia:** Resolução Colaborativa de Problemas  
008: **Objetivo de Aprendizagem:**  
009: - Descrever **ator**, **pré-condição**, **fluxo principal** e **fluxo alternativo** de indisponibilidade de uma quadra em um caso de uso de reserva.  
010: - Entender a estrutura de um caso de uso, com base em um sistema de reservas de quadras.  
011: 
012: ---
013: 
014: ## **1. Introdução (5 minutos)**
015: 
016: - Apresentar o tema da aula: **Casos de Uso – Reserva de uma Quadra Esportiva**.
017: - Contextualizar a importância de casos de uso na modelagem de sistemas.
018: - Introduzir os conceitos básicos: **ator**, **pré-condição**, **fluxo principal**, **fluxo alternativo**.
019: - Mostrar o **quadro de casos de uso** e a **folha de descrição do sistema** como materiais disponíveis para a aula.
020: 
021: ---
022: 
023: ## **2. Atividade de Introdução (10 minutos)**
024: 
025: - Distribuir o **quadro de casos de uso** e a **folha de descrição do sistema**.
026: - Pequenos grupos de 3 a 4 estudantes.
027: - Tarefa: Ler e compreender o sistema de reservas de quadras.
028: - Perguntas orientadoras:
029:   - Quem são os atores envolvidos?
030:   - O que é necessário para realizar uma reserva?
031:   - O que acontece se a quadra estiver indisponível?
032: 
033: ---
034: 
035: ## **3. Resolução Colaborativa de Problemas (25 minutos)**
036: 
037: ### **Passo 1: Identificar o Ator (5 minutos)**
038: 
039: - O ator envolvido nesse caso de uso é: **Usuário do sistema** (ex: aluno, professor, ou outro aluno).
040: - Compartilhar a definição de ator: **personagem que interage com o sistema**.
041: 
042: ### **Passo 2: Definir a Pré-Condição (5 minutos)**
043: 
044: - O que precisa ser verdade antes que o caso de uso possa ocorrer?
045: - Exemplo: O usuário precisa estar autenticado no sistema.
046: - Compartilhar a definição de pré-condição: **condição que deve ser atendida antes de iniciar o caso de uso**.
047: 
048: ### **Passo 3: Desenhar o Fluxo Principal (10 minutos)**
049: 
050: - O fluxo principal representa a **rotina normal** de reserva de uma quadra.
051: - Passos:
052:   1. O usuário entra no sistema.
053:   2. Ele seleciona uma quadra.
054:   3. Ele seleciona uma data e horário.
055:   4. O sistema verifica a disponibilidade.
056:   5. O sistema confirma a reserva.
057:   6. O usuário recebe confirmação.
058: 
059: - Compartilhar a definição de fluxo principal: **caminho de execução mais comum e esperado**.
060: 
061: ### **Passo 4: Identificar e Desenhar o Fluxo Alternativo (5 minutos)**
062: 
063: - O fluxo alternativo representa a **rotina que ocorre quando algo diferente acontece**.
064: - Exemplo: A quadra está indisponível.
065: - Passos:
066:   1. O usuário tenta reservar uma quadra.
067:   2. O sistema verifica a disponibilidade.
068:   3. A quadra está indisponível.
069:   4. O sistema notifica o usuário.
070:   5. O usuário tenta outra quadra ou data.
071: 
072: - Compartilhar a definição de fluxo alternativo: **caminho que ocorre quando a pré-condição não é satisfeita**.
073: 
074: ---
075: 
076: ## **4. Avaliação (5 minutos)**
077: 
078: - Entregar um **caso de uso** com os seguintes elementos:
079:   - **Atores**: Usuário do sistema
080:   - **Pré-condição**: O usuário está autenticado no sistema
081:   - **Fluxo principal**: Reserva de quadra com disponibilidade
082:   - **Fluxo alternativo**: Quadra indisponível
083: 
084: - Justificar a **condição que aciona o fluxo alternativo**:
085:   - A condição que aciona o fluxo alternativo é: **a quadra não está disponível no horário escolhido**.
086:   - Esta estratégia é usada para **tratar situações de falha ou inesperadas**, garantindo que o sistema informe o usuário de forma clara e útil.
087: 
088: ---
089: 
090: ## **5. Conclusão (5 minutos)**
091: 
092: - Resumir os conceitos aprendidos:
093:   - Ator, pré-condição, fluxo principal, fluxo alternativo.
094:   - A importância do caso de uso para modelar sistemas.
095: - Incentivar a reflexão: **Como o sistema pode melhorar a experiência do usuário em caso de indisponibilidade?**
096: 
097: ---
098: 
099: ## **Materiais e Recursos**
100: 
101: - **Quadro de casos de uso** (exemplo de estrutura)
102: - **Folha de descrição do sistema** (exemplo de sistema de reservas de quadras)
103: - **Folha de resposta com caso de uso** (para entrega)
104: 
105: ---
106: 
107: ## **Avaliação**
108: 
109: - O caso de uso elaborado pelos estudantes será a **estratégia de avaliação**.
110: - Ajustes podem ser feitos com base na compreensão do grupo.
111: 
112: ---
113: 
114: **Notas para o Professor:**
115: - Este plano pode ser adaptado para diferentes níveis de dificuldade.
116: - Pode ser usado como introdução a casos de uso ou como revisão de conceitos básicos.
117: - Recomenda-se a participação ativa dos alunos, com discussão e desenho dos fluxos.
