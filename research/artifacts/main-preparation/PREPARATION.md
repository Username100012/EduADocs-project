# Preparação offline do estudo principal

Plano do protocolo congelado; esta preparação não inicia a coleta nem valida os construtos.

12 tarefas autorais; quatro por disciplina; 36 prompts distintos (12 tarefas × três condições); 216 gerações previstas com dois geradores e três repetições; até 648 julgamentos se todas as gerações forem válidas.

O catálogo passou no esquema JSON e no modelo local; C1/C2 derivam da mesma instância de payload. Isso valida o contrato de software, não a qualidade das tarefas ou das métricas.

| Tarefa | Disciplina | Tópico | Referência SBC |
|---|---|---|---|
| task-001 | Algoritmos e Programação | Maior elemento de um vetor não vazio | C.1.3, p. 18 |
| task-002 | Algoritmos e Programação | Contagem de números pares em um vetor | C.1.3, p. 18 |
| task-003 | Algoritmos e Programação | Uma passagem de trocas adjacentes em ordenação por bolha | C.1.3, p. 18 |
| task-004 | Algoritmos e Programação | Operações de pilha com política LIFO | C.1.3, p. 18 |
| task-005 | Banco de Dados | Chaves primária e estrangeira em tabelas de pedidos | C.2.10, p. 22 |
| task-006 | Banco de Dados | INNER JOIN entre clientes e pedidos | C.2.10, p. 22 |
| task-007 | Banco de Dados | Agrupamento SQL com GROUP BY e COUNT | C.2.10, p. 22 |
| task-008 | Banco de Dados | Primeira forma normal e atributos multivalorados | C.2.10, p. 22 |
| task-009 | Engenharia de Software | Caso de uso de reserva de uma quadra esportiva | C.2.7, p. 22 |
| task-010 | Engenharia de Software | Critérios de aceitação de aplicação de cupom em uma compra | C.2.7, p. 22 |
| task-011 | Engenharia de Software | Particionamento de equivalência para validação de idade | C.2.8, p. 22 |
| task-012 | Engenharia de Software | Rastreabilidade entre requisitos e testes de um aplicativo de entregas | C.2.8, p. 22 |

Os tópicos, objetivos, duração, metodologia e aliases são escolhas autorais. O vínculo SBC é um recorte amplo e não equivale a validação, currículo obrigatório ou dificuldade equivalente.

## Mensuração e diagnóstico legado

O observador de campos detectou 84/84 campos nas renderizações literais. Isso verifica detecção sintática nos formatos testados, não cumprimento semântico, qualidade das tarefas ou validade pedagógica.

No diagnóstico lexical legado v2, 7/12 tarefas têm ao menos um estado não correspondente/indeterminado. Esses textos não são planos gerados. O diagnóstico foi preservado sem ajustar tarefas ou aliases; não é a definição de atendimento semântico.

- task-002: assessment_strategy.
- task-003: learning_objectives.
- task-004: learning_objectives.
- task-006: assessment_strategy.
- task-009: assessment_strategy.
- task-011: learning_objectives.
- task-012: assessment_strategy.

As observações sintáticas não usam aliases, heurísticas de negação ou conceitos do tópico para classificar atendimento. O contrato v2 reserva a estimativa semântica por requisito à julgadora, com evidências verificáveis; validar evidências não prova o acerto da estimativa.

## Condições de execução

- Verificar o selo e os hashes antes de chamadas reais; o runtime Ollama precisa corresponder ao digest/versão fixados.

O executor compartilhado aceita o plano de 12 tarefas e simulação, mas bloqueia coleta principal real enquanto a configuração estiver em rascunho. O plano prevê uso do Sol; a configuração ativa e os julgamentos anteriores não foram substituídos.
