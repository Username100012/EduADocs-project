# Fundamentação científica da avaliação computacional

Consulta em 19/10/2026. Esta nota organiza evidências e recomendações; não altera configurações, rubricas ou resultados e não autoriza novas coletas por si só. Os testes realizados até aqui são pilotos exploratórios.

## Evidências publicadas

| Trabalho revisado por pares | Evidência relevante | Limite para o EduADocs |
|---|---|---|
| Liu et al., G-Eval, EMNLP 2023 | Avaliação de texto por LLM com critérios explícitos, etapas de avaliação e preenchimento estruturado; estudo em sumarização e diálogo com comparação a avaliações humanas. | Não valida nossos quatro critérios, escala 1–4, planos de aula, português ou configuração Sol. O protocolo atual não é reprodução integral de G-Eval. |
| Zheng et al., NeurIPS 2023 | Examina julgadoras e limitações como vieses de posição, verbosidade, auto-favorecimento e raciocínio limitado. | Concordância entre repetições e uso de modelo forte não demonstram correção nem validade pedagógica. Resultados de GPT-4 no benchmark não se transferem automaticamente ao nosso estudo. |
| Tan et al., JudgeBench, ICLR 2025 | Constrói pares com rótulos de correção objetiva a partir de tarefas com gabarito/verificação, para avaliar a julgadora. | Sua avaliação de correção factual/lógica não é uma rubrica pedagógica. Nossos casos sintéticos são diagnósticos autorais inspiráveis por esse princípio, não reprodução do benchmark nem padrão-ouro validado. |

## Diagnóstico do trabalho atual

A literatura sustenta investigar LLMs como avaliadoras, mas não certifica os nossos escores. Os quatro critérios e âncoras atuais são uma operacionalização autoral. Precisam de justificativa específica e não devem ser apresentados como escala validada por G-Eval, MT-Bench ou JudgeBench.

O teste Mini/Sol comparou configurações com diferenças de raciocínio, amostragem e orçamento de saída. Os defeitos foram evidentes e restritos a três tarefas do próprio piloto. O resultado favorece o Sol nesse diagnóstico, sem estabelecer superioridade geral. Os dados não devem ser descartados nem transformados retroativamente em avaliação confirmatória.

## Proposta de protocolo para decidir antes de novas chamadas

As decisões seguintes são recomendações para o nosso recorte, não prescrições literais dos artigos:

1. Definir como objeto central o atendimento computacional de instruções, estrutura e comportamento operacional. Manter a LLM como estimativa semântica secundária, sem alegar eficácia pedagógica ou validação humana.
2. Mapear cada dimensão e cada nível da rubrica para evidências observáveis, explicitando o que é adaptado da literatura e o que é autoral. Se não houver fundamentação para um critério pedagógico, restringir sua interpretação, em vez de tratá-lo como validado.
3. Definir antecipadamente tarefas, controles C0/C1/C2, modelo/configuração e análise. A comparação C0/C1 envolve informação adicional; C1/C2 controla essa informação e varia sua organização.
4. Usar verificadores determinísticos onde houver decisão objetiva. Onde só há correspondência lexical, reportar proxy, incerteza e evidências; não chamar ausência de alias de descumprimento semântico.
5. Avaliar a julgadora em casos reservados com resultados verificáveis para os aspectos objetivos. Não ajustar e validar nos mesmos exemplos. Separar estabilidade, sensibilidade e correção; não escolher limiar de aprovação apenas para aprovar um modelo.
6. Fixar a regra de seleção e os resultados que serão reportados antes da coleta principal. Não alternar modelos e rubricas procurando diferenças favoráveis a C2. Preservar as limitações da avaliação exclusivamente computacional.

O próximo entregável recomendado é uma matriz única de **dimensão → definição → referência → operacionalização → métrica → limitação**, seguida do congelamento do protocolo. A referência científica pode ser selecionada agora; não é necessário gastar mais chamadas para isso.

Matriz entregue em 19/10/2026: [COMPUTATIONAL_EVALUATION_MATRIX.md](COMPUTATIONAL_EVALUATION_MATRIX.md), com exportação CSV e distinção entre referências, adaptações autorais, implementação atual e pendências. O protocolo ainda não é alterado automaticamente por esse documento.

## Referências

- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using Gpt-4 with Better Human Alignment*. EMNLP, pp. 2511–2522. DOI: [10.18653/v1/2023.emnlp-main.153](https://aclanthology.org/2023.emnlp-main.153/).
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS 36, Datasets and Benchmarks Track. [Anais oficiais](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html).
- Tan, S. et al. (2025). *JudgeBench: A Benchmark for Evaluating LLM-Based Judges*. ICLR 2025. [Anais oficiais](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9e720fce64f91114c49cfd640d821da3-Abstract-Conference.html), [artigo completo](https://proceedings.iclr.cc/paper_files/paper/2025/file/9e720fce64f91114c49cfd640d821da3-Paper-Conference.pdf).
