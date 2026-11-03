# Auditoria local de casos — 27/10/2026

Auditoria computacional exploratória após a coleta, realizada pelo assistente a pedido do pesquisador. Não é avaliação por participantes humanos, revisão de especialista independente, novo benchmark ou estimação de acurácia. Nenhuma API foi chamada. Nenhuma classificação original foi corrigida ou substituída.

## Escopo e procedimento

Foram reunidos os 72 planos Qwen3 de C1/C2 e os 216 registros de julgamento correspondentes para duração, incluindo falhas preservadas. Para objetivos, foram selecionados os 12 planos das tarefas 007 (GROUP BY/COUNT) e 012 (rastreabilidade), porque explicam diferenças já observadas. A seleção é pós-hoc e não permite estimar a prevalência de todos os tipos de erro.

Cada plano tem uma cópia com linhas numeradas. O arquivo cases.json contém o objetivo solicitado, hashes, resultados e evidências/justificativas literais dos julgamentos, além de diagnósticos de cronograma. O diagnóstico separa títulos e subtítulos, exclui extensões explicitamente opcionais e compara intervalos com rótulos de duração. Sua extração é exploratória e limitada à sintaxe reconhecida: não substitui o extrator congelado, não resolve automaticamente tempo de avaliações sem duração, sobreposições ou ambiguidades hierárquicas e não gera uma nova taxa de conformidade.

## Achados verificáveis

### 1. Problema real do plano: etapas de 55 minutos em aula de 50

Nos planos qwen3:task-007:c2:r1 e r2, as seis etapas indicam 5 + 10 + 20 + 10 + 5 + 5 = 55 minutos, embora o cabeçalho declare 50. As linhas 14, 28, 48, 63, 77 e 91 permitem reproduzir a soma. Os seis julgamentos válidos desses dois planos classificaram duração como contradicted. Aqui a divergência não é apenas um problema de extração de rótulos: existe inconsistência aritmética explícita no conteúdo.

### 2. Erro verificável da julgadora: soma incorreta

No plano qwen3:task-006:c1:r2, as cinco etapas indicam 5 + 25 + 10 + 5 + 5 = 50 minutos (linhas 13, 26, 60, 72 e 84). O julgamento eval-7fbc2ba0d368c3aef464d0894ce3f619 reproduz os mesmos valores, mas afirma que totalizam 55 e atribui contradicted. É um erro aritmético verificável da julgadora. Os outros dois julgamentos classificaram supported e calcularam 50 corretamente. O registro com erro permanece no resultado principal; este caso não estabelece uma taxa global de erro.

### 3. Problema real de hierarquia, com classificação variável

No plano qwen3:task-002:c2:r1, as seções principais somam 5 + 35 + 5 = 45 minutos, mas as etapas internas da prática somam 5 + 10 + 20 + 5 = 40, contrariando os 35 atribuídos à seção. Com essas etapas internas, o total seria 50. A inconsistência está no plano; os três julgamentos reconhecem a divergência, mas dois atribuem uncertain e um contradicted. Portanto, desacordo de categoria pode ocorrer mesmo quando a leitura dos números coincide. Não devemos converter essas duas categorias em uma única nota nem escolher a maioria.

### 4. Intervalos e rótulos incompatíveis

No plano qwen3:task-006:c2:r1, a tabela vai de 0 a 50 minutos, mas a primeira linha indica intervalo 0–5 e título Introdução (10 minutos); a segunda indica 5–15 e Aprendizagem Direta (20 minutos). Há duas incompatibilidades internas verificáveis. Todos os três julgamentos atribuem uncertain. Um total final de 50, isoladamente, não certifica consistência temporal.

### 5. Objetivo parcialmente atendido por detalhe específico

No plano qwen3:task-007:c2:r3, o objetivo e a atividade incluem GROUP BY/COUNT, contagem de pedidos e comparação do resultado com a tabela (linhas 21 e 71–74). Os três julgamentos atribuem partial porque não é explicitado que a tabela seja pequena, componente do objetivo solicitado. Isso não significa ausência de GROUP BY ou de conferência do resultado. A queda agregada em supported deve ser interpretada à luz desse componente específico, sem alegar que a consulta SQL esteja incorreta. Nos planos r1/r2 da mesma condição, as justificativas também discutem a conferência do resultado; não são todos o mesmo caso.

### 6. Objetivo declarado versus exemplo contraditório

No plano qwen3:task-012:c2:r1, o objetivo solicita identificar um requisito sem cobertura. A matriz das linhas 63–67 marca testes para R1, R2 e R3, inclusive R2/Teste 2; na linha 69, o texto afirma que R2 não tem teste associado. É uma contradição direta entre matriz e explicação. A proposta de Teste 6 da linha 71 também repete o Teste 5 da linha 52.

A julgadora não ignorou completamente esse defeito: os três julgamentos deram alinhamento instrucional 2 e coerência textual 1. Entretanto, no requisito learning_objectives, dois atribuíram supported por considerar a declaração do objetivo e deslocar a inconsistência para os critérios secundários; um atribuiu contradicted por considerar o exemplo parte da execução do objetivo. Assim, há instabilidade na aplicação do limite entre presença do objetivo e realização coerente da tarefa. Não é possível usar supported como sinônimo de correção do exemplo ou validade pedagógica.

## Implicações para o artigo

Os resultados combinam defeitos do material, ambiguidade de aplicação das categorias e pelo menos um erro aritmético demonstrável da julgadora. A comparação C1/C2 permanece descritiva e mista: esta auditoria não transforma os achados em superioridade geral de uma condição e não altera a análise principal. Repetir a mesma julgadora três vezes permite observar estabilidade, mas não garante correção; as três repetições também podem compartilhar o mesmo limite interpretativo.

Não recalculamos notas com rótulos escolhidos pelo assistente, não criamos estimativa de precisão da julgadora e não modificamos o protocolo após observar os resultados. Uma futura versão pode separar explicitamente representação do requisito, coerência de sua execução e verificações aritméticas determinísticas, mas isso exigiria novo contrato e dados separados.

### Texto sugerido para resultados/limitações

Uma auditoria computacional exploratória dos casos identificou inconsistências temporais nos planos e limitações do julgamento automatizado. Em um plano, seis etapas somaram 55 minutos apesar da duração declarada de 50. Em outro, a julgadora classificou a duração como contraditória ao somar incorretamente 5, 25, 10, 5 e 5 minutos como 55, embora o total fosse 50. Também foram observadas diferenças de classificação entre a representação explícita de objetivos e a consistência dos exemplos associados. Esses casos mostram que a correspondência literal das citações e a repetição dos julgamentos não asseguram correção semântica, motivo pelo qual os resultados são apresentados como estimativas automatizadas e não como validação pedagógica.

## Índice dos 72 planos e diagnósticos

As somas são saídas do diagnóstico exploratório, não classificações de conformidade. Ausência de extração não significa ausência de cronograma.

| Plano | Soma de etapas selecionadas | Soma de intervalos | Rótulos incompatíveis com intervalos |
|---|---:|---:|---:|
| [qwen3:task-001:c1:r1](qwen3_task-001_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-001:c1:r2](qwen3_task-001_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-001:c1:r3](qwen3_task-001_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-001:c2:r1](qwen3_task-001_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-001:c2:r2](qwen3_task-001_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-001:c2:r3](qwen3_task-001_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-002:c1:r1](qwen3_task-002_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-002:c1:r2](qwen3_task-002_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-002:c1:r3](qwen3_task-002_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-002:c2:r1](qwen3_task-002_c2_r1.md) | 45 | não extraído | 0 |
| [qwen3:task-002:c2:r2](qwen3_task-002_c2_r2.md) | 55 | não extraído | 0 |
| [qwen3:task-002:c2:r3](qwen3_task-002_c2_r3.md) | 45 | não extraído | 0 |
| [qwen3:task-003:c1:r1](qwen3_task-003_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-003:c1:r2](qwen3_task-003_c1_r2.md) | 40 | não extraído | 0 |
| [qwen3:task-003:c1:r3](qwen3_task-003_c1_r3.md) | 45 | não extraído | 0 |
| [qwen3:task-003:c2:r1](qwen3_task-003_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-003:c2:r2](qwen3_task-003_c2_r2.md) | não extraído | 50 | 0 |
| [qwen3:task-003:c2:r3](qwen3_task-003_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-004:c1:r1](qwen3_task-004_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-004:c1:r2](qwen3_task-004_c1_r2.md) | 55 | não extraído | 0 |
| [qwen3:task-004:c1:r3](qwen3_task-004_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-004:c2:r1](qwen3_task-004_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-004:c2:r2](qwen3_task-004_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-004:c2:r3](qwen3_task-004_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-005:c1:r1](qwen3_task-005_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-005:c1:r2](qwen3_task-005_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-005:c1:r3](qwen3_task-005_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-005:c2:r1](qwen3_task-005_c2_r1.md) | 45 | não extraído | 0 |
| [qwen3:task-005:c2:r2](qwen3_task-005_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-005:c2:r3](qwen3_task-005_c2_r3.md) | 45 | não extraído | 0 |
| [qwen3:task-006:c1:r1](qwen3_task-006_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-006:c1:r2](qwen3_task-006_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-006:c1:r3](qwen3_task-006_c1_r3.md) | 40 | não extraído | 0 |
| [qwen3:task-006:c2:r1](qwen3_task-006_c2_r1.md) | não extraído | 50 | 2 |
| [qwen3:task-006:c2:r2](qwen3_task-006_c2_r2.md) | não extraído | 50 | 2 |
| [qwen3:task-006:c2:r3](qwen3_task-006_c2_r3.md) | não extraído | 50 | 3 |
| [qwen3:task-007:c1:r1](qwen3_task-007_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-007:c1:r2](qwen3_task-007_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-007:c1:r3](qwen3_task-007_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-007:c2:r1](qwen3_task-007_c2_r1.md) | 55 | não extraído | 0 |
| [qwen3:task-007:c2:r2](qwen3_task-007_c2_r2.md) | 55 | não extraído | 0 |
| [qwen3:task-007:c2:r3](qwen3_task-007_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-008:c1:r1](qwen3_task-008_c1_r1.md) | 55 | não extraído | 0 |
| [qwen3:task-008:c1:r2](qwen3_task-008_c1_r2.md) | 55 | não extraído | 0 |
| [qwen3:task-008:c1:r3](qwen3_task-008_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-008:c2:r1](qwen3_task-008_c2_r1.md) | 45 | não extraído | 0 |
| [qwen3:task-008:c2:r2](qwen3_task-008_c2_r2.md) | 40 | não extraído | 0 |
| [qwen3:task-008:c2:r3](qwen3_task-008_c2_r3.md) | 40 | não extraído | 0 |
| [qwen3:task-009:c1:r1](qwen3_task-009_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-009:c1:r2](qwen3_task-009_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-009:c1:r3](qwen3_task-009_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-009:c2:r1](qwen3_task-009_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-009:c2:r2](qwen3_task-009_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-009:c2:r3](qwen3_task-009_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-010:c1:r1](qwen3_task-010_c1_r1.md) | 55 | não extraído | 0 |
| [qwen3:task-010:c1:r2](qwen3_task-010_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-010:c1:r3](qwen3_task-010_c1_r3.md) | 55 | não extraído | 0 |
| [qwen3:task-010:c2:r1](qwen3_task-010_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-010:c2:r2](qwen3_task-010_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-010:c2:r3](qwen3_task-010_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-011:c1:r1](qwen3_task-011_c1_r1.md) | 45 | não extraído | 0 |
| [qwen3:task-011:c1:r2](qwen3_task-011_c1_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-011:c1:r3](qwen3_task-011_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-011:c2:r1](qwen3_task-011_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-011:c2:r2](qwen3_task-011_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-011:c2:r3](qwen3_task-011_c2_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-012:c1:r1](qwen3_task-012_c1_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-012:c1:r2](qwen3_task-012_c1_r2.md) | 55 | não extraído | 0 |
| [qwen3:task-012:c1:r3](qwen3_task-012_c1_r3.md) | 50 | não extraído | 0 |
| [qwen3:task-012:c2:r1](qwen3_task-012_c2_r1.md) | 50 | não extraído | 0 |
| [qwen3:task-012:c2:r2](qwen3_task-012_c2_r2.md) | 50 | não extraído | 0 |
| [qwen3:task-012:c2:r3](qwen3_task-012_c2_r3.md) | 50 | não extraído | 0 |

## Objetivos: distribuições dos 12 planos selecionados

| Plano | Supported | Partial | Contradicted | Julgamentos inválidos |
|---|---:|---:|---:|---:|
| qwen3:task-007:c1:r1 | 3 | 0 | 0 | 0 |
| qwen3:task-007:c1:r2 | 3 | 0 | 0 | 0 |
| qwen3:task-007:c1:r3 | 3 | 0 | 0 | 0 |
| qwen3:task-007:c2:r1 | 0 | 3 | 0 | 0 |
| qwen3:task-007:c2:r2 | 0 | 3 | 0 | 0 |
| qwen3:task-007:c2:r3 | 0 | 3 | 0 | 0 |
| qwen3:task-012:c1:r1 | 0 | 0 | 3 | 0 |
| qwen3:task-012:c1:r2 | 2 | 0 | 0 | 1 |
| qwen3:task-012:c1:r3 | 0 | 0 | 3 | 0 |
| qwen3:task-012:c2:r1 | 2 | 0 | 1 | 0 |
| qwen3:task-012:c2:r2 | 3 | 0 | 0 | 0 |
| qwen3:task-012:c2:r3 | 3 | 0 | 0 | 0 |
