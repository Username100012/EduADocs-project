# Mapeamento curricular do piloto — Ciência da Computação

Fonte: Zorzo et al. (2017), *Referenciais de Formação para os Cursos de Graduação em
Computação*, SBC, ISBN 978-85-7669-424-3. Consultado em 15/10/2026.
[Documento publicado pela SBC, depositado na PUCRS](https://repositorio.pucrs.br/dspace/bitstream/10923/22180/2/Referenciais_de_Formao_para_os_Cursos_de_Graduao_em_Computao.pdf).

Foi consultado o capítulo II (Ciência da Computação), seção II.6. O documento distingue
conteúdos de disciplinas (p. 17). O mapeamento abaixo utiliza paráfrases, sem transcrever
as competências. As páginas indicadas são as impressas, iguais à posição no PDF contado
a partir de 1.

| Tarefa | Vínculo no referencial | Operacionalização autoral |
|---|---|---|
| pilot-001 | C.1.3, p. 18; eixo Resolução de Problemas; conteúdo Algoritmos/Técnicas de Programação | Busca linear em vetor: produzir pseudocódigo e testar presença e ausência |
| pilot-002 | C.2.10, p. 22; eixo Desenvolvimento de Sistemas; conteúdo Banco de Dados | Consultas SELECT/WHERE em uma tabela: escrever consultas e prever resultados |
| pilot-003 | C.2.7, p. 22; eixo Desenvolvimento de Sistemas; conteúdo Engenharia de Software | Especificar requisitos de uma biblioteca e definir condições de verificação |

## Decisões do piloto

Os sete requisitos completos e o mapeamento legível por máquina estão no único arquivo
de configuração, `experiments/pilot_config.json`, versão `eduadocs-pilot-v2-sbc-cc`.
Este documento apenas explica as decisões. Os tópicos específicos, os objetivos de aula,
os pré-requisitos, os recursos e as avaliações são adaptações dos pesquisadores. Não
foram prescritos nem validados pela SBC. Cada aula cobre parte de uma competência.

Para reduzir variação incidental, as três tarefas adotam nível superior introdutório,
50 minutos, resolução colaborativa de problemas, quadro e material impresso. O piloto
não pressupõe que elas tenham dificuldade equivalente e não atribui semestre obrigatório.
As áreas foram escolhidas intencionalmente para variar o tipo de artefato esperado:
algoritmo, consulta e especificação textual. Não representam todo o curso.

## Objetivo → avaliação → evidência computacional

- **Programação:** objetivo de construir e testar; avaliação pede pseudocódigo e testes
  de mesa; procurar menções aos dois casos e ao procedimento. Sem executar ou formalizar
  o pseudocódigo, não concluir correção algorítmica.
- **Banco de Dados:** objetivo de consultar e determinar resultados; avaliação pede duas
  consultas; identificar SELECT, WHERE e resultados esperados. Sem banco e casos de
  teste de referência, não concluir correção das consultas.
- **Engenharia de Software:** objetivo de especificar e justificar; avaliação pede quatro
  requisitos e verificações; identificar esses elementos. As expressões “não funcional”
  e “funcional” devem ser diferenciadas; substring simples produziria falsos positivos.

Aliases e palavras-chave são indícios de presença textual, não provas de atendimento
semântico. Verificações semânticas registradas nas tarefas documentam o recorte, sem
alterar silenciosamente a rubrica da julgadora. Questões como adequação dos exemplos,
alinhamento das atividades e compatibilidade com o nível pertencem à estimativa semântica
secundária, com suas limitações.

## Controles preservados

Permanecem 3 tarefas × 3 condições × 3 repetições = 27 gerações planejadas. C1 e C2 são
construídos da mesma instância dos sete requisitos; C0 recebe somente tipo de material
e tópico. O mapeamento curricular não entra como instrução adicional exclusiva de C2.
Os pré-requisitos são contexto de construção das tarefas e não um oitavo campo enviado
ao modelo. O modelo gerador ainda precisa ser definido antes das chamadas.

O recorte curricular não substitui a fundamentação metodológica da avaliação. O livro
é uma referência institucional de formação, não um estudo experimental que valide
métricas de geração por LLM. Nenhum resultado empírico foi produzido nesta etapa.
