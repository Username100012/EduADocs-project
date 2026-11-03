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
017: - **Contexto:**  
018:   - Cupons são usados para descontos em compras.
019:   - O sistema precisa validar se o cupom é válido e não expirado.
020:   - O objetivo é criar regras que determinam se um cupom pode ser aplicado.
021: 
022: - **Materiais:**  
023:   - Quadro com regras de uso de cupons em um carrinho de compras.  
024:   - Folha com exemplos de cupons (válidos, expirados, com data de expiração).  
025:   - Pincel e papel para anotações.  
026: 
027: ---
028: 
029: ## **2. Atividade de Resolução Colaborativa (30 minutos)**
030: 
031: **Objetivo:** Identificar e formalizar os critérios de aceitação de cupons (válido e expirado) no formato **Dado Quando Então**.
032: 
033: ### **Passo 1: Análise de Cenários (5 minutos)**
034: 
035: - **Perguntas para orientação:**  
036:   - O que caracteriza um **cupom válido**?  
037:   - O que caracteriza um **cupom expirado**?  
038:   - Como o sistema verifica a data de expiração?  
039: 
040: **Respostas esperadas (aproximadas):**  
041: - **Cupom válido:** Data de expiração maior que a data atual.  
042: - **Cupom expirado:** Data de expiração menor ou igual à data atual.
043: 
044: ---
045: 
046: ### **Passo 2: Definição dos Critérios (15 minutos)**
047: 
048: **Grupo de trabalho:**  
049: - Os alunos são divididos em grupos de 3 a 4 pessoas.  
050: - Cada grupo deve definir **dois critérios de aceitação** para cupons:  
051:   1. **Cupom válido**  
052:   2. **Cupom expirado**  
053: 
054: **Instruções:**  
055: - Use o **formato Dado Quando Então**.  
056: - Justifique os critérios com base nas regras de uso de cupons.  
057: - Use o quadro como referência para verificar se os critérios estão alinhados.  
058: 
059: **Exemplo de modelo:**  
060: - **Dado:** O cupom tem data de expiração.  
061: - **Quando:** A data atual é menor que a data de expiração.  
062: - **Então:** O cupom é válido.  
063: 
064: ---
065: 
066: ### **Passo 3: Apresentação dos Resultados (10 minutos)**
067: 
068: - Cada grupo apresenta seus **dois critérios de aceitação**.  
069: - O professor avalia se os critérios estão corretos e está alinhados com as regras do sistema.  
070: - Os critérios são registrados no quadro para serem revisados em conjunto.  
071: 
072: ---
073: 
074: ## **3. Avaliação (10 minutos)**
075: 
076: **Estratégia de Avaliação:**  
077: - **Cenário 1:** Cupom válido  
078:   - **Dado:** Data de expiração do cupom é 30/06/2025.  
079:   - **Quando:** Data atual é 15/06/2025.  
080:   - **Então:** O cupom é válido.  
081: 
082: - **Cenário 2:** Cupom expirado  
083:   - **Dado:** Data de expiração do cupom é 10/06/2025.  
084:   - **Quando:** Data atual é 15/06/2025.  
085:   - **Então:** O cupom é expirado.  
086: 
087: **Justificativa:**  
088: - O sistema compara a data de expiração do cupom com a data atual.  
089: - Se a data atual está antes da data de expiração → cupom é válido.  
090: - Se a data atual está depois ou igual à data de expiração → cupom é expirado.  
091: 
092: ---
093: 
094: ## **4. Conclusão (5 minutos)**
095: 
096: **Resumo:**  
097: - Os alunos aprenderam a especificar critérios de aceitação de cupons em formato **Dado Quando Então**.  
098: - Compreenderam a importância de definir regras claras para validar cupons.  
099: - Fizeram uma análise prática de como um sistema de compras pode verificar a validade de um cupom.  
100: 
101: **Pergunta de reflexão final:**  
102: *“Como poderíamos expandir esses critérios para incluir cupons com código de verificação?”*
103: 
104: ---
105: 
106: ## **5. Recursos Utilizados:**
107: 
108: - Quadro com regras de uso de cupons.  
109: - Folha com exemplos de cupons.  
110: - Pincel e papel para anotações.  
111: 
112: ---
113: 
114: ## **6. Referências (opcional):**
115: 
116: - **Livros e artigos:**  
117:   - *Introdução à Programação* – Robert Sedgewick  
118:   - *Principios de sistemas de informação* – Richard L. Daft  
119: - **Materiais complementares:**  
120:   - Diagramas de fluxo para validação de cupons.  
121:   - Exemplos de código em Python para validação de datas.
122: 
123: ---
124: 
125: **Plano finalizado com sucesso!**  
126: Se quiser, posso ajudar a adaptar isso para um **formato de aula em videoconferência** ou para **atividade em grupo presencial**.
