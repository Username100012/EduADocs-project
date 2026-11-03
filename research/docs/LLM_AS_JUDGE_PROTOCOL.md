# Protocolo de LLM como julgadora do EduADocs

## 1. Papel no experimento

A LLM julgadora é uma métrica automática secundária. As métricas determinísticas de
conformidade, falha e desempenho permanecem como resultados primários. A pontuação da
julgadora não constitui verdade de referência, avaliação docente ou evidência de eficácia
pedagógica.

O protocolo segue a avaliação por critérios e formulário estruturado proposta no G-Eval
(Liu et al., 2023) e incorpora controles para os vieses de posição, verbosidade e
autopreferência discutidos por Zheng et al. (2023).

## 2. Unidade de julgamento

Cada resposta será avaliada individualmente (*pointwise*). A julgadora receberá:

- a descrição da tarefa e seus sete requisitos;
- uma única resposta anonimizada;
- a rubrica e os descritores das notas;
- a instrução de retornar somente o objeto JSON definido pelo esquema.

Não serão informados condição experimental, modelo gerador, provedor, custo ou latência.
O texto não poderá conter rótulos C0, C1 ou C2 durante o julgamento.

## 3. Critérios semânticos

Cada critério recebe uma nota inteira de 1 a 4.

### 3.1 Fidelidade semântica à tarefa (`semantic_fidelity`)

- `1`: contradiz ou ignora a maior parte dos requisitos fornecidos;
- `2`: representa alguns requisitos, mas contém omissões ou incompatibilidades relevantes;
- `3`: representa os requisitos centrais, com pequenas omissões ou imprecisões;
- `4`: representa de forma completa e compatível todos os requisitos fornecidos.

### 3.2 Alinhamento instrucional interno (`instructional_alignment`)

- `1`: objetivos, atividades/metodologia e avaliação são ausentes ou incompatíveis;
- `2`: há relações parciais, mas pelo menos um componente central está desconectado;
- `3`: os componentes são majoritariamente coerentes, com lacunas pontuais;
- `4`: objetivos, atividades/metodologia e avaliação estão explicitamente alinhados.

Essa medida é uma operacionalização automática do alinhamento construtivo. Ela não
comprova qualidade pedagógica nem aprendizagem.

### 3.3 Adequação declarada ao nível educacional (`grade_appropriateness`)

- `1`: linguagem, complexidade ou atividades são claramente incompatíveis com o nível;
- `2`: há vários elementos inadequados ou sem adaptação suficiente;
- `3`: o material é majoritariamente compatível, com inadequações pontuais;
- `4`: linguagem, complexidade e atividades são consistentemente compatíveis.

### 3.4 Coerência e exequibilidade interna (`coherence_feasibility`)

- `1`: plano fragmentado, contraditório ou inexequível nas condições declaradas;
- `2`: sequência parcialmente compreensível, com contradições ou obstáculos relevantes;
- `3`: sequência coerente e executável, com pequenas lacunas;
- `4`: sequência clara, internamente coerente e executável com tempo e recursos descritos.

A julgadora não pontuará correção factual sem fontes externas autorizadas. Essa dimensão
exigirá um protocolo separado de fundamentação e não será inferida por conhecimento
paramétrico da própria julgadora.

## 4. Saída estruturada

Para cada critério, a resposta deverá conter `score` inteiro entre 1 e 4 e uma
`justification` curta baseada em evidências observáveis no texto. A LLM devolverá também
`evaluation_id` e `rubric_version`. O futuro executor anexará `judge_model`,
`judge_model_version` e `run_id`; esses dados operacionais não serão confiados à LLM.

O contrato exato está em `experiments/llm_judge_response.schema.json`, e o prompt
versionado em `src/experiment/judge_prompt.py`. O esquema não solicita média ou nota
global: qualquer agregação será calculada posteriormente por código determinístico.

Resultados que não validarem contra o esquema JSON serão registrados como falha de
julgamento e repetidos conforme política previamente congelada. Não haverá correção
manual.

O parser local (`src/experiment/judge_response.py`) aceita exatamente um objeto JSON.
Blocos Markdown, texto antes ou depois do JSON, chaves duplicadas e coerção silenciosa
não são aceitos. As falhas recebem categorias estáveis: resposta vazia, JSON inválido,
chave duplicada, raiz não objetiva, campo obrigatório ausente, campo inesperado, versão
incompatível, identificador inválido ou divergente, nota inválida, justificativa inválida
e violação genérica do esquema. O conteúdo original deverá ser preservado pelo futuro
executor para auditoria.

Cada tentativa será representada pelo registro imutável e versionado definido em
`src/experiment/judge_record.py`. O registro preserva tarefa, condição, repetição,
identificador da geração de origem, prompt completo, resposta candidata, hashes SHA-256,
configuração da julgadora, metadados operacionais, resposta bruta e, de forma mutuamente
exclusiva, resultado validado ou erro classificado. A condição fica no registro analítico,
mas não é inserida no prompt da julgadora. O `evaluation_id` enviado ao modelo é opaco e
não codifica tarefa, condição, modelo ou repetição. Credenciais são proibidas inclusive dentro de
dicionários aninhados de parâmetros e metadados.

Os registros serão persistidos por `src/experiment/judge_record_logger.py` em JSONL
append-only, com um objeto por linha. A busca por `record_id` duplicado e a escrita são
executadas sob o mesmo bloqueio de arquivo. Depois da escrita, o arquivo é sincronizado
com o sistema operacional. Linhas vazias, JSON inválido, raiz diferente de objeto ou
ausência de `record_id` tornam o log inválido e interrompem novas gravações; nenhum dado
preexistente é corrigido, removido ou ignorado silenciosamente.

O manifesto de execução é definido em `src/experiment/judge_manifest.py`. Ele congela a
configuração explícita do modelo julgador, três repetições por resposta, no máximo duas
tentativas por repetição, preservação de todas as tentativas, ausência de substituição de
repetições falhas, política de cegamento e hashes dos seis artefatos metodológicos. O
manifesto é imutável, possui hash canônico e só pode ser salvo por criação exclusiva; um
arquivo existente não é sobrescrito. O manifesto final não será criado com aliases ou
placeholders: provedor, modelo e versão deverão ser decididos e registrados antes da
primeira execução.

## 5. Configuração e repetição

- usar como julgador principal o snapshot `gpt-5.4-mini-2026-03-17`, conforme a
  justificativa registrada em `docs/JUDGE_MODEL_SELECTION.md`;
- usar o mesmo modelo julgador e a mesma versão em todo o experimento principal;
- preferir família diferente da empregada pelo modelo gerador;
- fixar temperatura em `0` ou no menor valor permitido pelo provedor;
- realizar três julgamentos independentes por resposta;
- preservar respostas brutas e metadados de todas as tentativas;
- agregar por mediana e reportar dispersão e concordância entre repetições;
- executar análise de sensibilidade com um segundo julgador somente como resultado
  secundário, caso o orçamento permita.

## 6. Auditoria computacional da julgadora

Antes do experimento principal, a configuração da julgadora deverá passar por testes
metamórficos com casos sintéticos congelados, sem avaliação humana:

1. **Anonimização:** trocar identificadores neutros não deve alterar as notas.
2. **Duplicação:** entradas textualmente idênticas devem produzir as mesmas notas.
3. **Posição:** quando houver teste pareado auxiliar, inverter a ordem dos candidatos não
   deve inverter a preferência substantiva.
4. **Verbosidade:** acrescentar conteúdo redundante e irrelevante não deve aumentar a
   pontuação.
5. **Omissão controlada:** remover um requisito explicitamente atendido não deve aumentar
   `semantic_fidelity`.
6. **Desalinhamento controlado:** substituir a avaliação por procedimento incompatível
   com o objetivo não deve aumentar `instructional_alignment`.

As taxas de consistência desses testes serão reportadas. Eventual limiar de aceitação
deverá ser definido no manifesto antes de executar respostas experimentais.

## 7. Uso nas conclusões

As notas serão descritas como estimativas de uma julgadora automática. Diferenças entre
C0, C1 e C2 não serão apresentadas como superioridade pedagógica comprovada. Formulação
admissível:

> A condição obteve maior conformidade determinística e maior pontuação semântica segundo
> a rubrica automatizada e a configuração de LLM julgadora especificadas.

## 8. Referências metodológicas

- Liu, Y. et al. *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*.
  EMNLP, 2023. DOI: 10.18653/v1/2023.emnlp-main.153.
- Zheng, L. et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*.
  NeurIPS, 2023.
- Ribeiro, M. T. et al. *Beyond Accuracy: Behavioral Testing of NLP Models with
  CheckList*. ACL, 2020. DOI: 10.18653/v1/2020.acl-main.442.
- Biggs, J. *Enhancing Teaching through Constructive Alignment*. Higher Education,
  32, 347–364, 1996. DOI: 10.1007/BF00138871.
