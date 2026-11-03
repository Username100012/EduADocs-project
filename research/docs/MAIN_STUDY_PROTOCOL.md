# Protocolo do estudo principal — eduadocs-main-v1.0.0

Versão local fechada em 25/10/2026, antes da coleta principal e informada pelo piloto já analisado. Não é pré-registro externo, ensaio confirmatório ou validação pedagógica. A fonte única de configuração e catálogo é `experiments/main_config.json`; seu selo é `main_config.json.sha256`. O objeto `freeze` registra os hashes dos artefatos definidores, do catálogo e do plano de prompts. Este documento não executa chamadas.

## Pergunta, comparação e escopo

Examinar, descritivamente, como a organização de instruções com a mesma informação afeta observações estruturais, duração numérica extraível, operação e estimativas semânticas automáticas de planos de aula. Comparação principal: C1 versus C2 dentro de cada gerador e tarefa. Empates e resultados desfavoráveis a C2 são admissíveis e não motivarão mudanças de escala, modelo ou tarefas.

C0 contém exclusivamente tipo de material e tópico. C1 apresenta os sete requisitos em um parágrafo; C2 apresenta exatamente os mesmos valores em seções e lista de parâmetros. As duas derivam da mesma instância de `LessonPlanSemanticPayload`, com equivalência informacional testada. Os templates são `lesson-plan-c0-generic-v1.0.0`, `lesson-plan-c1-free-text-v1.0.0` e `lesson-plan-c2-structured-v1.0.0`. C0/C1 varia a informação disponível e não isola estrutura; não é ablação individual dos sete requisitos.

Não se avaliam SUS, aprendizagem, eficácia em sala, adequação pedagógica global, segurança ou correção factual/algorítmica sistemática. Não haverá participantes humanos nem coleta de seus dados. Os demais módulos do EduADocs não fazem parte deste experimento.

## Catálogo e recorte

Doze tarefas autorais e intencionais: quatro de Algoritmos e Programação, quatro de Banco de Dados e quatro de Engenharia de Software. Nível introdutório de graduação em Ciência da Computação; português, admitidos termos técnicos em inglês; 50 minutos; resolução colaborativa de problemas; quadro e folhas impressas. Os sete requisitos são tópico, nível, objetivos, duração, metodologia, materiais e estratégia de avaliação.

| Tarefa | Área | Tópico e limite |
|---|---|---|
| task-001 | Algoritmos | Máximo de vetor inteiro não vazio; negativos e empates. |
| task-002 | Algoritmos | Contagem de pares, inclusive vetor vazio e sem pares. |
| task-003 | Algoritmos | Uma passagem esquerda-direita de trocas adjacentes para ordem crescente. |
| task-004 | Algoritmos | Pilha LIFO: push, pop, topo e remoção em pilha vazia. |
| task-005 | Banco de Dados | Chaves primária/estrangeira e integridade referencial em clientes/pedidos. |
| task-006 | Banco de Dados | INNER JOIN de duas tabelas, inclusive cliente sem pedidos. |
| task-007 | Banco de Dados | GROUP BY e COUNT em uma tabela; linhas versus grupos. |
| task-008 | Banco de Dados | Atomicidade de telefones e primeira forma normal no domínio do exercício. |
| task-009 | Engenharia de Software | Caso de uso textual de reserva; fluxo principal e alternativa de indisponibilidade. |
| task-010 | Engenharia de Software | Dois critérios Dado-Quando-Então: cupom válido/expirado. |
| task-011 | Engenharia de Software | Partições de idade inteira: <0, 0–120, >120; sem parsing ou tipos não inteiros. |
| task-012 | Engenharia de Software | Rastreabilidade de três requisitos e testes, com uma lacuna de cobertura. |

Os pré-requisitos e os limites foram revisados e estão em `tasks[].scope_review`. São metadados explicativos, não um oitavo requisito: não são enviados ao gerador nem à julgadora. Os payloads e os prompts foram preservados em relação ao planejamento anterior. Vetores, tabelas e regras concretas não são fixtures literais fornecidas: a LLM concretiza os exemplos. Não se afirmam dificuldade equivalente, representatividade curricular ou poder estatístico.

O mapeamento amplo utiliza o capítulo II, seção II.6, dos [referenciais SBC 2017](https://repositorio.pucrs.br/dspace/bitstream/10923/22180/2/Referenciais_de_Formao_para_os_Cursos_de_Graduao_em_Computao.pdf), competências C.1.3 (p. 18), C.2.7, C.2.8 e C.2.10 (p. 22). As tarefas e seus requisitos são escolhas autorais, não prescrições ou validação pela SBC. Os tópicos diferem dos três pilotos, com sobreposição de disciplinas e conceitos; não se alega independência curricular.

## Volume, modelos e execução

- 12 tarefas × três condições × três gerações × dois geradores = **216 gerações**, 108 por gerador e 36 por condição em cada gerador.
- Até **648 julgamentos**, três por resposta elegível. As repetições não aumentam o número de tarefas independentes.
- Gerador remoto: `gemini-3.8-flash`, Google GenAI SDK 1.56.0, `max_output_tokens=4096`, thinking low, texto livre; temperatura/top_p/top_k/seed omitidos. O teto inclui raciocínio e texto.
- Gerador local: `qwen3:4b-q4_K_M`, Ollama 0.17.1, digest `2bfd38a7daaf4b1037efe517ccb73d1a3bbd4822cf89f1a82be1569050a114e0`; temperatura 0,7, seed 42, contexto 8192, saída até 4096, think false e keep_alive 10m. Hardware de referência: i7-10870H, cerca de 64 GB de RAM e RTX 2060 de 6 GB. O executor confere digest e versão antes de chamadas locais; não baixa nem substitui pesos.
- Julgadora: `gpt-6.1-sol`, Responses API, raciocínio low, máximo total 4096, JSON estrito, store false, sem temperatura, top_p ou seed explícitos. Identificadores comerciais sem snapshot datado não garantem imutabilidade: registrar modelo retornado, data e parâmetros efetivos.

O plano completo tem ordem pseudoaleatória fixa com seed 42. Gerações são sequenciais, sem ferramentas, histórico, instrução de sistema adicional ou esquema imposto ao gerador. O executor avalia o texto original, antes de exportação DOCX. A seleção de um gerador por comando conserva a ordem relativa de seus itens, registra o subplano e deve usar diretório próprio, sem misturar logs incompatíveis.

Julgamentos usam até seis requisições simultâneas, com identificadores opacos, alvo completo e candidato numerado por linhas. Condição e gerador não são enviados explicitamente; o conteúdo pode revelar características da condição. A ordem da fila é determinística pelos IDs opacos. Concorrência e latência são registradas; não comparar esses tempos como se todos os julgamentos fossem sequenciais.

O orçamento Gemini, calculado a partir de 36 prompts únicos medidos por countTokens, prevê 12.663 tokens de entrada e até 442.368 de saída no total. Com preços Standard consultados em 25/10/2026, câmbio de planejamento R$ 6/US$ e reserva de 25%, estima R$ 12,52. R$ 30 é referência flexível, não limite obrigatório. Julgamentos OpenAI usam saldo separado; o estudo não autoriza recargas automáticas. Reavaliar preços fora da vigência informada, preservando a metodologia ou versionando mudanças necessárias.

## Mensuração congelada

**Principais, computacionais:** observador `eduadocs-requirement-observations-v1`, com detected, empty e not_detected para campos rotulados; declarações temporais numéricas e intervalos HH:MM reconhecidos; latência mediana/IQR inclusivo, tokens reportados, custos estimados com fonte/data, tamanho textual e falhas. O extrator não soma arbitrariamente durações em títulos de etapas. Ausência de extração ou contradição detectada não prova consistência. As proxies lexicais `eduadocs-textual-proxies-v2` são auxiliares e não definem atendimento semântico.

**Secundários, estimativas da julgadora:** contrato `eduadocs-requirement-judge-v2.0.0`, esquema `eduadocs-requirement-judge-response-v2.0.0`, prompt `lesson-plan-requirement-judge-v2.0.0`. Cada um dos sete requisitos recebe supported, partial, not_addressed, contradicted ou uncertain, justificativa e evidências conforme o [contrato v2](REQUIREMENT_JUDGE_CONTRACT_V2.md). A igualdade de citações com linhas completas da origem é literal, incluindo espaços. Não relaxar esse critério após a coleta nem reparar respostas. Uma citação verdadeira não demonstra pertinência ou acerto semântico.

Somente duas escalas ordinais autorais de 1 a 4: `instructional_alignment` e `textual_coherence`, com âncoras incluídas no prompt selado. Não há nota global de fidelidade, adequação pedagógica ou viabilidade real em sala.

## Elegibilidade, falhas e parada

Tentativa única por geração e por julgamento, sem retries automáticos. Geração elegível para julgamento: status success, término STOP/stop e texto não vazio. Outputs non_stop/truncados permanecem nos indicadores operacionais e observações textuais, identificados pelo status; não entram na análise semântica secundária. Falha sem texto não recebe nota zero. Reportar a cobertura por tarefa, condição e gerador antes de comparar conteúdo.

Erro de geração interrompe o comando, preservando os itens concluídos. Em julgamento, erros de schema/citação são classificados, preservados e não repetidos; o lote continua para os itens ainda não chamados. Erros de API/transporte, recusa, resposta incompleta ou modelo divergente impedem novas ondas após registrar as chamadas já iniciadas. Retomar processa somente IDs ainda não concluídos. Início sem resultado bloqueia repetição automática: a chamada pode ter consumido créditos e exige diagnóstico.

Não haverá recuperação automática de falhas, substituição de planos, troca de modelo, ajuste de prompt, extensão de limite ou aumento de amostra por resultados desfavoráveis. A recuperação manual dos dois 401 no piloto foi exceção documentada anterior a este protocolo, não política geral de reposição. Uma mudança necessária após iniciar a coleta exige nova versão explícita e dados separados.

## Análise descritiva

1. Tarefa é a unidade de comparação. Mostrar cada tarefa e área, separando os geradores. Repetições com seed fixa podem ser idênticas; reportar quantidade de textos distintos e não tratar planos ou julgamentos como tarefas independentes.
2. Campos sintáticos: contagens/proporções dos três estados entre textos analisáveis, com falhas e textos ausentes separados. Duração: separar valores extraídos, correspondência com alvo, contradições detectadas e indeterminados; sem tolerância adicional escolhida após os resultados.
3. Categorias semânticas: todas as frequências, por requisito, com denominadores de julgamentos válidos e de planos. Concordância exata somente em trincas válidas completas. Não converter em pontos, mediana, nota composta ou veredito por maioria. Distribuições de julgamento não são proporções de planos independentes nem acurácia.
4. Escalas ordinais: mediana de três julgamentos válidos por plano, mediana dos planos completos de cada tarefa/condição/gerador e mediana entre tarefas com pesos iguais. Reportar valores por tarefa, amplitude, concordância exata, cobertura e notas máximas. Trincas incompletas não recebem mediana. Áreas permanecem visíveis.
5. Contraste principal C1/C2 pareado por tarefa dentro de cada gerador, apenas onde houver dados comparáveis; informar ausências e não imputar. Não aplicar testes de significância, limiar de aprovação, RCS/CS/OR ou score global. Não selecionar retrospectivamente o indicador mais favorável a C2.
6. Latências e tokens são resumidos descritivamente com cobertura. Custos não reportados permanecem desconhecidos; faltas não viram zero. Família, hardware, quantização e configurações não são isolados na comparação entre provedores.

## Evidência anterior e limites científicos

O piloto de três tarefas e um gerador, os 80 julgamentos v2 válidos e a rodada diagnóstica de 18 respostas são dados anteriores, excluídos dos 216 planos principais. O diagnóstico satisfez seis relações predefinidas em um tópico sintético de fila FIFO, incluindo defeitos explícitos. Casos foram inspecionados no desenvolvimento, sem cegamento por terceiros; isso não estima acurácia geral ou validação pedagógica. O piloto apresentou resultados mistos para C1/C2 e informou decisões metodológicas: o presente documento não constitui pré-registro independente desses achados.

A decomposição de requisitos é informada por [FollowBench, ACL 2024](https://aclanthology.org/2024.acl-long.257/); a avaliação por critérios por [G-Eval, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.153/); limitações da julgadora por [Zheng et al., NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) e [JudgeBench, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9e720fce64f91114c49cfd640d821da3-Abstract-Conference.html); alinhamento conceitual por [Biggs, 1996](https://doi.org/10.1007/BF00138871). Não se transfere a validação humana desses trabalhos para nossas escalas. Definições operacionais e limites das fontes: [matriz científica](COMPUTATIONAL_EVALUATION_MATRIX.md).

## Integridade e comandos Windows

Configuração, catálogo, plano de prompts e fontes definidoras têm hashes verificados antes de chamadas reais. O selo detecta divergências locais; não fornece timestamp externo nem garante reprodução de modelos hospedados. Logs JSONL têm bloqueio, flush/fsync e detecção de IDs/eventos duplicados. Dados do piloto mantêm seu snapshot original de configuração. Chaves permanecem fora dos artefatos, com prioridade ao `.env` local e fallback ao ambiente. Não sobrescrever o diretório do piloto com dados principais.

Conferência offline do selo:

```powershell
.\.venv\Scripts\python.exe scripts/freeze_main_study.py
```

Preparação local, sem gerar conteúdo:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_main_study.py
```

O passo futuro de coleta, **não executado pelo congelamento**, usará diretório novo:

```powershell
.\.venv\Scripts\python.exe scripts/run_pilot.py --config experiments/main_config.json --output artifacts/main-study-v1 --live
```

Após concluir as gerações, preparar a fila a partir dos textos originais e executar os julgamentos segundo a política congelada:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_requirement_judgments.py artifacts/main-study-v1 --output artifacts/main-judgments-v1
.\.venv\Scripts\python.exe scripts/run_requirement_judgments.py artifacts/main-study-v1 artifacts/main-judgments-v1 --live --max-jobs 648 --workers 6 --continue-validation-errors
.\.venv\Scripts\python.exe scripts/observe_saved_requirements.py artifacts/main-study-v1
.\.venv\Scripts\python.exe scripts/report_requirement_results.py artifacts/main-study-v1 artifacts/main-judgments-v1
```

Executar comandos de geração/julgamento requer chamadas pagas; nenhum deles foi iniciado nesta revisão. Alterações em artefatos selados requerem revisão de versão e preservação do histórico, nunca atualização silenciosa do selo após a coleta.
