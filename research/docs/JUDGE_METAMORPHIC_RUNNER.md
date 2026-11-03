# Executor local de simulação metamórfica

`src/experiment/metamorphic_runner.py` executa somente fixtures sintéticas. Não tem
adaptador de provedor nem chave de API. Usa o construtor real do prompt e o parser real
de respostas. Todos os registros e relatórios carregam `simulated: true`.

Exemplo em PowerShell, na raiz do projeto:

```powershell
$env:PYTHONPATH = "src"
python -m experiment.metamorphic_runner --output artifacts/metamorphic-simulation-001 --scenario expected
```

A pasta de saída deve ser nova. Serão criados `attempts.jsonl` e `report.json`. Nenhum
arquivo anterior é sobrescrito. O log é exclusivo desta simulação; não utiliza condições
C0/C1/C2 nem o esquema de registros experimentais de geração.

Há quatro cenários de software: `expected`, `constant`, `violations` e `incomplete`.
As notas são valores programados, não evidência empírica de um julgador. Os cenários
verificam relações satisfeitas, uma julgadora constante, violações e falhas de parsing.

O identificador de execução deriva do hash do conjunto, seed e cenário. Identificadores
opacos de avaliação e identificadores de registro são distintos. Duplicatas de consistência
compartilham exatamente o prompt e o identificador de avaliação; membro, repetição e
tentativa são distinguidos localmente. A ordem das 72 chamadas simuladas é embaralhada
com seed registrada. Cada erro de parsing admite uma segunda tentativa e ambas ficam
preservadas. O manifesto congelado anterior não é alterado nem usado para apresentar
esta simulação como execução do modelo selecionado.

O relatório traz medianas por membro/critério, amplitude e concordância entre repetições,
diferenças, direção das diferenças e relação satisfeita por par. Apresenta denominadores,
pares incompletos e falhas; não imputa notas aos incompletos. Uma julgadora constante
aparece como empate, mesmo quando satisfaz a relação fraca de não aumento.

Antes de chamadas reais, ainda será necessário vincular esses registros ao manifesto da
auditoria metamórfica, registrar a revisão do código, congelar a ordem e configurar o
adaptador do modelo. A simulação não testa compatibilidade com a API nem validade das notas.
