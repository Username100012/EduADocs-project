001: **Plano de Aula: Rastreabilidade entre Requisitos e Testes de um Aplicativo de Entregas**
002: 
003: ---
004: 
005: **1. Dados Gerais**
006: 
007: - **Disciplina:** Engenharia de Software  
008: - **Nível:** Graduação em Ciência da Computação – Formação Introdutória  
009: - **Tópico:** Rastreabilidade entre requisitos e testes de um aplicativo de entregas  
010: - **Duração:** 50 minutos  
011: - **Metodologia:** Resolução colaborativa de problemas  
012: - **Objetivo de Aprendizagem:** Construir uma matriz relacionando três requisitos de entregas aos testes que os verificam e identificar um requisito sem cobertura  
013: - **Avaliação:** Entregar a matriz requisito-teste e propor um teste para o requisito sem cobertura, justificando a correspondência  
014: 
015: ---
016: 
017: **2. Estrutura do Plano de Aula**
018: 
019: **I. Introdução (5 minutos)**
020: 
021: - **Objetivo da aula:** Introduzir o conceito de rastreabilidade entre requisitos e testes, destacando sua importância na garantia da qualidade de software.
022: - **Contexto:** Aplicativo de entregas, como uma plataforma de logística, com requisitos específicos para a funcionalidade de rastreamento, entrega e notificação.
023: - **Perguntas de motivação:**
024:   - Por que é importante verificar que cada requisito está coberto por testes?
025:   - Como identificar requisitos que não estão sendo testados?
026: 
027: **II. Explicação teórica (5 minutos)**
028: 
029: - **Definição de requisitos:** Especificações que definem o comportamento esperado do sistema.
030: - **Casos de teste:** Situações que permitem verificar se os requisitos estão sendo atendidos.
031: - **Rastreabilidade:** Relacionamento entre requisitos e testes, garantindo que cada requisito seja verificado.
032: - **Requisito sem cobertura:** Um requisito que não está sendo testado, o que pode levar a falhas no sistema.
033: 
034: **III. Atividade Prática (35 minutos)**
035: 
036: **Material:**  
037: - Quadro com três requisitos de entregas  
038: - Folha com casos de teste associados a esses requisitos  
039: 
040: **Requisitos apresentados:**
041: 
042: 1. **Requisito 1:** O sistema deve permitir que o entregador rastreie a posição do pacote em tempo real.  
043: 2. **Requisito 2:** O sistema deve notificar o cliente quando o pacote estiver chegando.  
044: 3. **Requisito 3:** O sistema deve permitir que o cliente faça uma solicitação de reembolso em caso de atraso na entrega.  
045: 
046: **Casos de teste apresentados:**
047: 
048: 1. Teste 1: Verificação da posição do pacote em tempo real  
049: 2. Teste 2: Notificação do cliente quando o pacote estiver chegando  
050: 3. Teste 3: Simulação de reembolso após atraso na entrega  
051: 4. Teste 4: Verificação de posição do pacote em tempo real após mudança de rota  
052: 5. Teste 5: Notificação do cliente com aviso de atraso
053: 
054: **Atividade:**
055: 
056: - Os alunos trabalham em grupos de 3 a 4 pessoas.
057: - Cada grupo recebe os requisitos e os casos de teste.
058: - O objetivo é construir uma **matriz requisito-teste**, relacionando os requisitos aos casos de teste que os verificam.
059: - Após a construção da matriz, os alunos identificam **um requisito sem cobertura** e propõem um **caso de teste** que cobre esse requisito, justificando a correspondência.
060: 
061: **Exemplo de matriz:**
062: 
063: | Requisito | Teste 1 | Teste 2 | Teste 3 | Teste 4 | Teste 5 |
064: |----------|---------|---------|---------|---------|---------|
065: | R1       | ✔       | ❌      | ❌      | ✔       | ❌      |
066: | R2       | ❌      | ✔       | ❌      | ❌      | ❌      |
067: | R3       | ❌      | ❌      | ✔       | ❌      | ❌      |
068: 
069: **Requisito sem cobertura:** R2 (Notificação do cliente quando o pacote estiver chegando) – não tem nenhum teste associado.
070: 
071: **Proposta de teste para R2:** Teste 6: Notificação do cliente com aviso de atraso.
072: 
073: **Justificativa:** O teste 6 verifica a funcionalidade de notificação do cliente em situações de atraso, que está relacionada ao requisito de notificação quando o pacote estiver chegando.
074: 
075: **IV. Conclusão e Discussão (5 minutos)**
076: 
077: - **Resumo da aula:** A rastreabilidade entre requisitos e testes é essencial para garantir que todos os requisitos do sistema sejam verificados.
078: - **Reflexão:** Como podemos evitar requisitos sem cobertura em projetos futuros?
079: - **Avaliação:** Os alunos entregam a matriz requisito-teste e a proposta de teste para o requisito sem cobertura.
080: 
081: ---
082: 
083: **3. Recursos Utilizados**
084: 
085: - Quadro de whiteboard  
086: - Folha com requisitos e casos de teste  
087: - Lápis, caneta e papel para anotações
088: 
089: ---
090: 
091: **4. Avaliação**
092: 
093: - **Forma:** Trabalho em grupo com entrega de matriz requisito-teste e proposta de teste para requisito sem cobertura.  
094: - **Criterios de avaliação:**  
095:   - Precisão na relação entre requisitos e testes  
096:   - Identificação correta de requisito sem cobertura  
097:   - Justificativa clara e lógica da proposta de teste  
098: 
099: ---
100: 
101: **5. Extensão (opcional)**
102: 
103: - Para alunos que desejarem, pode-se propor a criação de um diagrama de rastreabilidade mais completo ou a elaboração de um relatório técnico sobre a importância do rastreabilidade no ciclo de vida de um software.
104: 
105: --- 
106: 
107: **Fim do plano de aula**
