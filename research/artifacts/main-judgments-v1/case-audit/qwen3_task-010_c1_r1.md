001: **Plano de Aula: Critérios de Aceitação de Aplicação de Cupom em Uma Compra**  
002: **Nível:** Graduação em Ciência da Computação  
003: **Formação:** Introdutória  
004: **Duração:** 50 minutos  
005: **Metodologia:** Resolução colaborativa de problemas  
006: **Objetivo de Aprendizagem:** Especificar dois critérios de aceitação no formato **Dado Quando Então** para cupom válido e cupom expirado, justificando os resultados observáveis.  
007: 
008: ---
009: 
010: ## **1. Introdução (5 minutos)**
011: 
012: **Objetivo:** Contextualizar a importância dos critérios de aceitação de cupons em sistemas de compra.
013: 
014: - **Pergunta inicial:**  
015:   *“Como um sistema de compras sabe se um cupom é válido ou expirado?”*
016: 
017: - **Explicação breve:**  
018:   Os critérios de aceitação são regras que definem under quais condições um cupom pode ser aplicado ou não. São fundamentais para garantir a funcionalidade e a segurança do sistema.
019: 
020: - **Materiais necessários:**  
021:   - Quadro de anotações  
022:   - Folha com regras de uso de cupons  
023:   - Exemplos de cupons válidos e expirados  
024:   - Canetas, marcadores, papel
025: 
026: ---
027: 
028: ## **2. Atividade de Introdução (10 minutos)**
029: 
030: **Objetivo:** Introduzir os conceitos de cupons válidos e expirados.
031: 
032: - **Explicação sobre cupons:**  
033:   - Um **cupom válido** é aquele que ainda está dentro do período de validade.  
034:   - Um **cupom expirado** é aquele que ultrapassou a data de validade.
035: 
036: - **Exemplo prático:**  
037:   - Cupom A: “10% OFF até 31/12/2024”  
038:   - Cupom B: “10% OFF até 01/01/2023”  
039: 
040: - **Perguntas para reflexão:**  
041:   - Como você saberia se um cupom é válido ou não?  
042:   - O que aconteceria se um cupom expirado fosse aplicado?
043: 
044: ---
045: 
046: ## **3. Resolução Colaborativa de Problemas (25 minutos)**
047: 
048: **Objetivo:** Os alunos trabalham em grupos para definir os critérios de aceitação de cupons no formato **Dado Quando Então**.
049: 
050: ### **Materiais disponíveis:**
051: - **Quadro de anotações** para registrar as regras.  
052: - **Folha com regras de uso de cupons** (exemplo: data de validade, código do cupom, tipo de produto, etc.)
053: 
054: ### **Passo a passo:**
055: 
056: 1. **Dividir os alunos em grupos de 3 a 4 pessoas.**  
057: 2. **Distribuir uma folha com regras de uso de cupons.**  
058: 3. **Incentivar os alunos a discutir e definir regras para validação de cupons.**  
059: 4. **Cada grupo deve criar dois critérios de aceitação no formato **Dado Quando Então**.**  
060: 5. **Avaliação: Distinguir cupom válido vs. cupom expirado.**
061: 
062: ---
063: 
064: ### **Exemplo de Regras de Uso de Cupons (para orientação dos alunos):**
065: 
066: | Campo            | Descrição                          |
067: |------------------|------------------------------------|
068: | Código do cupom  | String de 6 caracteres             |
069: | Data de validade | Data no formato “DD/MM/AAAA”       |
070: | Data atual       | Data do sistema (ex: 25/10/2024)   |
071: | Tipo de produto  | String (ex: “varejo”, “online”)    |
072: 
073: ---
074: 
075: ### **Exemplo de Cenário 1: Cupom Válido**
076: 
077: **Dado:**  
078: - Código do cupom: “AB1234”  
079: - Data de validade: 31/12/2024  
080: - Data atual: 25/10/2024  
081: 
082: **Quando:**  
083: - O sistema verifica a data de validade do cupom.  
084: 
085: **Então:**  
086: - O cupom é considerado **válido** e pode ser aplicado.
087: 
088: **Resultado esperado:**  
089: - O sistema permite a aplicação do cupom.
090: 
091: ---
092: 
093: ### **Exemplo de Cenário 2: Cupom Expirado**
094: 
095: **Dado:**  
096: - Código do cupom: “CD5678”  
097: - Data de validade: 01/01/2023  
098: - Data atual: 25/10/2024  
099: 
100: **Quando:**  
101: - O sistema verifica a data de validade do cupom.  
102: 
103: **Então:**  
104: - O cupom é considerado **expirado** e não pode ser aplicado.
105: 
106: **Resultado esperado:**  
107: - O sistema não permite a aplicação do cupom.
108: 
109: ---
110: 
111: ## **4. Apresentação e Discussão (10 minutos)**
112: 
113: **Objetivo:** Os grupos apresentam seus critérios de aceitação e justificam os resultados.
114: 
115: - Cada grupo apresenta um **Dado Quando Então** para cupom válido e outro para expirado.  
116: - Os demais alunos analisam a validade dos critérios.  
117: - Discussão sobre:  
118:   - Como os critérios podem ser implementados em código?  
119:   - Quais são os possíveis erros ou limitações?  
120:   - Como garantir a precisão do sistema?
121: 
122: ---
123: 
124: ## **5. Conclusão e Avaliação (5 minutos)**
125: 
126: **Objetivo:** Sintetizar o aprendizado e avaliar a compreensão dos alunos.
127: 
128: - **Resumo:**  
129:   - Critérios de aceitação são regras que definem se um cupom pode ser aplicado.  
130:   - O formato **Dado Quando Então** é uma maneira clara e usável de descrever essas regras.  
131:   - A validade do cupom depende da comparação entre a data de validade e a data atual.
132: 
133: - **Avaliação:**  
134:   - Cada grupo recebe uma pontuação com base na clareza, precisão e justificativa de seus critérios.  
135:   - O professor avalia a aplicação correta do formato **Dado Quando Então** e a justificativa dos resultados.
136: 
137: ---
138: 
139: ## **6. Extensão (opcional)**
140: 
141: - **Desafio adicional:**  
142:   - Crie um **fluxo de execução** (flowchart) para o sistema que verifica se um cupom é válido ou não.  
143:   - Explique como isso poderia ser implementado em linguagem de programação (ex: Python, Java, etc.).
144: 
145: ---
146: 
147: ## **Recursos Utilizados:**
148: 
149: - **Quadro e folha com regras de uso de cupons**  
150: - **Exemplos de cupons**  
151: - **Papel e canetas**  
152: - **Perguntas guia para discussão**
153: 
154: ---
155: 
156: **Nota:** Este plano de aula busca desenvolver habilidades de **modelagem de regras**, **resolução de problemas colaborativa** e **comunicação de conceitos técnicos**, alinhados com os objetivos da disciplina de Ciência da Computação.
