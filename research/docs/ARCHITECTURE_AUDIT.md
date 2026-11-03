# Auditoria do fluxo arquitetural do EduADocs

## Escopo

Esta auditoria verifica o fluxo do módulo de plano de aula em relação à Figura 1 da
qualificação. A avaliação é estrutural e computacional; o SUS não integra este escopo.

## Resultado por componente

| Componente da figura | Evidência na implementação | Situação |
|---|---|---|
| Apresentação | `app.py` coleta configurações e seleciona o modelo | Implementado |
| Parametrização pedagógica | `pedagogical.lesson_plan_request_from_form` produz `GenerationRequest` | Implementado |
| Construção da instrução | `prompting.build_lesson_plan_prompt` produz artefato versionado e hash | Implementado |
| Integração Multi-LLM | `ProviderGateway` seleciona um dos quatro adaptadores | Implementado |
| Seleção e chamada | adaptador correspondente ao provedor escolhido | Implementado |
| Processamento | resposta bruta preservada e conteúdo normalizado | Implementado |
| Apresentação e exportação | visualização Streamlit e exportador DOCX independente | Implementado |
| Registro transversal | `ExecutionRecord` persistido em JSONL | Implementado |

## Achado corrigido durante a auditoria

Embora as camadas estivessem presentes, o gerador do plano de aula ainda coordenava
diretamente chamada, processamento, exportação e registro. Copiar esse fluxo para os
outros módulos produziria duplicação e risco de comportamentos divergentes.

A sequência foi extraída para `application.execute_generation`. Os geradores passam a
ser adaptadores finos: criam a solicitação e o prompt do material e delegam o restante ao
pipeline compartilhado.

## Pendências controladas

- O custo estimado permanece nulo até a definição de uma tabela de preços versionada.
- Tokens podem ser nulos quando o provedor não os informa.
- A execução local via Hugging Face ainda pertence ao fluxo legado; Ollama é o adaptador
  local da arquitetura principal.
- Os quatro módulos foram migrados para o pipeline comum.
- Os geradores antigos de Resumo e PowerPoint, que não pertenciam à interface nem ao
  escopo científico, foram removidos juntamente com `api_handler.py`.

## Resultado final da migração dos módulos

Plano de aula, notas de aula, lista de exercícios e mapa mental possuem modelos de
parâmetros específicos, prompts versionados e exportadores configurados. Todos utilizam
o mesmo serviço de aplicação, o mesmo gateway Multi-LLM, o mesmo processamento e o
mesmo registro reprodutível. Os arquivos em `generators/` são apenas adaptadores finos
para preservar temporariamente o contrato da interface Streamlit.
