# Contribuição e posicionamento do estudo principal

Versão para revisão dos autores — 28/10/2026. Não constitui afirmação de ineditismo; a distinção frente aos trabalhos relacionados precisa ser sustentada no manuscrito.

## Pergunta central

Como a apresentação em texto livre ou estruturado dos mesmos sete requisitos se relaciona com o atendimento estimado desses requisitos, a consistência textual e os indicadores operacionais da geração de planos de aula em português?

## Contribuição proposta

O estudo apresenta uma avaliação computacional reproduzível do EduADocs, com 12 tarefas introdutórias de Computação, dois geradores e condições de instrução com informação controlada no contraste C1/C2. Integra classificações nominais por requisito, duas medidas ordinais secundárias e indicadores de latência e tokens. A auditoria documenta separadamente limitações do extrator e da julgadora, com evidências rastreáveis e preservação dos resultados originais.

A apresentação estruturada teve resultados distintos entre requisitos e tarefas e não demonstrou superioridade geral sobre texto livre com o mesmo conteúdo informacional. C2 apresentou menores medianas de latência e tokens de saída nas configurações executadas; não se atribui esse resultado exclusivamente à sintaxe, pois o tamanho das instruções e das respostas e as condições de execução também diferem. Uma análise pós-coleta com pares de casos completos não inverteu as direções dos contrastes nominais agrupados nem alterou as medianas gerais, mantendo a interpretação descritiva sob essa regra de seleção.

## Formulação sugerida para a conclusão

Os resultados indicam que a estruturação de instruções informacionalmente equivalentes não produziu benefício uniforme no atendimento estimado dos requisitos. Foram observadas diferenças localizadas, especialmente em materiais, e menores medianas de latência e tokens de saída em C2 nas configurações avaliadas. A interpretação de resultados mistos foi mantida em análise complementar com casos completos pareados. Entretanto, a auditoria identificou inconsistências nos planos e um erro aritmético da julgadora, demonstrando que validação estrutural e evidências literais não garantem correção semântica. A contribuição do estudo reside na caracterização reproduzível desses comportamentos e limites, sem alegar eficácia pedagógica, equivalência entre condições ou superioridade geral de uma estratégia de prompt.

## Alegações que os dados não sustentam

- C2 é geralmente superior a C1 ou equivalente a C1.
- As frequências nominais são acurácia, notas de qualidade ou proporções de planos independentes.
- Usar outra família como julgadora elimina vieses ou valida o conteúdo.
- Os 645 julgamentos constituem 645 unidades experimentais independentes.
- A ausência de inversão no recorte completo prova ausência de viés dos dados ausentes.
- Os resultados de planos de aula generalizam aos demais módulos, currículos ou eficácia em sala.

## Encaminhamento editorial

O rascunho de resultados e limitações está em ARTICLE_MAIN_RESULTS_AND_LIMITATIONS.md. O contraste principal deve ser C1/C2; C0 contextualiza o acréscimo de informação. A auditoria é uma análise exploratória pós-coleta, não uma nova medida principal nem um benchmark de acurácia. Nenhum novo experimento é necessário para incorporar estes resultados ao manuscrito; a força da contribuição ainda deve ser confrontada com os trabalhos relacionados e o escopo da submissão.
