# Casos metamórficos da julgadora

Conjunto sintético versionado: `experiments/judge_metamorphic_cases.v1.json`.
Transformações locais: `src/experiment/judge_metamorphic.py`.

São três tarefas (Ciências, Matemática e Língua Portuguesa), cada uma com quatro pares.
Cada par preserva exatamente o mesmo payload de sete requisitos para as duas respostas.
Os textos foram construídos para testar o mecanismo de avaliação, não como referências
de qualidade pedagógica validadas. Não há participantes nem notas humanas.

| Transformação | Alteração do candidato | Relação esperada |
|---|---|---|
| Consistência | Nenhuma; texto idêntico | Igualdade em cada um dos quatro critérios |
| Verbosidade | Acrescentar redundância editorial sem conteúdo instrucional | Nenhum critério deve aumentar |
| Omissão | Remover somente a seção de recursos | Fidelidade semântica não deve aumentar |
| Desalinhamento | Trocar somente a avaliação por tarefa de outro domínio | Alinhamento instrucional não deve aumentar |

As transformações seguem testes de invariância e expectativa direcional como os de
CheckList (Ribeiro et al., ACL 2020,
https://aclanthology.org/2020.acl-main.442/). A verificação de verbosidade é motivada
pelos vieses relatados por Zheng et al. (NeurIPS 2023,
https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html).
Essas fontes motivam a metodologia; não validam estes doze casos específicos.

## Plano de execução futura

Avaliar separadamente os dois membros de cada par, com três julgamentos de cada membro:
12 pares × 2 membros × 3 julgamentos = 72 respostas de julgamento planejadas, antes de
novas tentativas. Não reutilizar o baseline entre pares. Ordenar as chamadas com uma
permutação pseudoaleatória registrada, mantendo a tabela de correspondências fora do
prompt. Não apresentar o tipo de transformação ou a relação esperada à julgadora.

Para consistência, manter exatamente o mesmo prompt, inclusive o identificador opaco,
entre duplicatas; distinguir membros e repetições apenas nos metadados locais. Esses
casos precisam de identificadores próprios de auditoria: não devem ser registrados como
condições C0/C1/C2 fictícias. O executor metamórfico ainda não foi implementado.

## Análise previamente definida

Reportar notas por critério e por chamada. Agregar cada membro pela mediana de suas três
notas válidas. Comparar a mediana do variante à do baseline e calcular a proporção de
pares que satisfazem cada relação, com denominador explícito por transformação.

Além da relação fraca de não aumento, reportar separadamente redução estrita, empate e
aumento. Um julgador constante satisfaria não aumento, mas não discriminaria as
degradações. Também reportar concordância exata e amplitude das notas entre repetições.
Não interpretar concordância automática como concordância com professores.

Pares com menos de três julgamentos válidos em qualquer membro serão classificados como
incompletos, sem imputar notas ou excluí-los silenciosamente: apresentar falhas e a
proporção de pares completos sobre os 12 planejados. Preservar todas as tentativas.

Este conjunto é uma auditoria exploratória pequena. Não foi estabelecido um limiar
numérico para declarar a julgadora aprovada, nem se pretende inferência de validade
pedagógica a partir de três casos por transformação. Ajustes posteriores exigem nova
versão, sem sobrescrever o conjunto utilizado.

## Integridade e testes locais

O hash dos bytes do JSON está em `experiments/judge_metamorphic_cases.v1.sha256`.
Os seis artefatos do manifesto anterior foram preservados. O conjunto novo e o código
metamórfico precisarão ser incluídos na identificação da execução antes de chamadas reais.

```bash
python3 -m unittest tests.test_judge_metamorphic tests.test_llm_judge_manifest -v
```

Os testes verificam a estrutura das alterações e a preservação do manifesto. Não
executam nem simulam notas como se fossem resultados de uma LLM.
