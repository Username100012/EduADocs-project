# Sensibilidade da julgadora a defeitos controlados

Teste diagnóstico separado do piloto. Não altera a rubrica, o modelo, os parâmetros ou as notas anteriores. Usa `scripts/run_judge_sensitivity.py`, a configuração já selecionada para GPT e o mesmo esquema/parser local.

## Desenho definido antes das chamadas

São três planos sintéticos construídos a partir dos payloads das tarefas de Computação do piloto. Não são novas tarefas independentes nem planos gerados pelo Qwen3. Cada plano tem os sete requisitos explícitos, um procedimento compatível com a tarefa e etapas de 5 + 15 + 20 + 10 = 50 minutos.

Cada base origina três variantes:

| Variante | Única alteração textual | Critério-alvo | Relação esperada |
|---|---|---|---|
| Omissão | Retirada da linha de materiais | Fidelidade semântica | Mediana menor que a base |
| Desalinhamento | Avaliação substituída por grafia de capitais brasileiras | Alinhamento interno | Mediana menor que a base |
| Contradição temporal | Prática de 20 passa para 70 minutos; total de etapas passa a 100 e duração declarada permanece 50 | Coerência/exequibilidade | Mediana menor que a base |

São 12 textos × três julgamentos = 36 chamadas, em ordem embaralhada com seed 42. A base é compartilhada pelas três comparações de cada tarefa. Os quatro critérios são sempre julgados; o critério-alvo e a direção da comparação são definidos antecipadamente, sem exigir uma nota absoluta “correta” para a base.

Os identificadores de avaliação são opacos. Os rótulos de variante não são enviados à julgadora. O cabeçalho do JSONL contém os candidatos, payloads, prompts, configuração, esquema e relações esperadas. Cada chamada gera eventos de início e resultado com resposta bruta e validação local. Há bloqueio de arquivo, flush/fsync e retomada sem repetir resultados; um início sem resultado impede duplicação automática. Não há tentativas automáticas.

## Executar e consolidar no Windows

```powershell
.\.venv\Scripts\python.exe scripts/run_judge_sensitivity.py --output artifacts/judge-sensitivity-v1 --live
.\.venv\Scripts\python.exe scripts/run_judge_sensitivity.py --output artifacts/judge-sensitivity-v1 --summarize
```

Sem as opções `--live` ou `--summarize`, apenas se confere o plano, sem chamadas. O relatório é `artifacts/judge-sensitivity-v1/RESULTS.md`; notas dos quatro critérios, dispersão, completude e consumo ficam em `report.json`, e o registro integral em `judgments.jsonl`.

Empate não é queda estrita. Resultados incompletos não são classificados como sucesso nem recebem zero. Um julgador constante com nota 4 em tudo produziria nove empates: esse comportamento foi verificado em teste simulado. Essa separação evita confundir a antiga relação fraca “não aumentar” com evidência de sensibilidade ao defeito.

## Alcance

São perturbações autorais, deliberadas e evidentes. Uma avaliação completamente fora do tema ou um cronograma de 100 minutos em vez de 50 é um teste simples; detectar esses casos não comprova percepção de erros sutis ou validade da rubrica no uso real. O efeito pode atingir mais de um critério; os resultados completos são preservados para inspecionar efeitos cruzados.

As repetições e comparações compartilham conteúdo e não são independentes. Não há participantes humanos, validação factual, eficácia pedagógica, nota composta ou testes de significância. Qualquer revisão posterior deve ser versionada, mantendo estes resultados e reservando casos novos para verificar as mudanças. A suíte antiga `judge_metamorphic_cases.v1.json` permanece congelada e não é substituída por este teste.

## Resultado de 17/10/2026

Foram concluídas 36/36 chamadas válidas: seis comparações com queda estrita e três empates. O desalinhamento reduziu a mediana de alinhamento de 4 para 1 nas três tarefas; a contradição temporal reduziu coerência/exequibilidade de 4 para 1 nas três. A omissão dos materiais manteve fidelidade em 4 nas três tarefas e nos nove julgamentos individuais.

As justificativas de fidelidade nos casos de omissão citam outros requisitos e não discutem a ausência dos materiais. Isso demonstra falta de penalização para esta omissão no teste, sem permitir inferir como o modelo processou internamente a ausência. O critério de fidelidade não deve ser usado como evidência de cumprimento integral dos sete requisitos.

Recomendação: manter os resultados e revisar, em etapa separada e versionada, a verificação de fidelidade por requisito; verificar a nova versão em casos reservados. O bom desempenho nos defeitos evidentes de tempo/alinhamento não elimina o erro aritmético encontrado no piloto nem valida a julgadora em geral. Suíte completa Windows: 171 testes aprovados. Nenhuma resposta ou nota do piloto foi alterada.
