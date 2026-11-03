# Modelos de dados da arquitetura EduADocs

## Objetivo

Este documento registra a primeira etapa da adequação da aplicação à arquitetura
Multi-LLM apresentada na qualificação. A etapa introduz uma representação formal e
independente de provedor para a solicitação de geração.

Nenhuma tela ou função de geração existente foi alterada nesta etapa. Os modelos foram
adicionados em paralelo ao fluxo atual para permitir uma migração incremental e segura.

## Fronteira arquitetural

O modelo `GenerationRequest` será o contrato entre as seguintes camadas:

```text
Camada de apresentação
        ↓
Parametrização pedagógica
        ↓ GenerationRequest
Construção das instruções
        ↓
Integração Multi-LLM
```

O objeto não executa chamadas externas, não constrói prompts e não cria documentos.
Sua responsabilidade é representar e validar os dados que atravessam as camadas.

## Arquivos criados

- `src/models/generation_request.py`: enumerações e modelos de entrada.
- `src/models/__init__.py`: interface pública do pacote.
- `tests/test_generation_request.py`: testes unitários dos contratos.

## GenerationRequest

O modelo comum contém:

- identificador único e data da execução;
- tipo de material;
- disciplina, tópico, nível educacional e idioma;
- provedor e identificador do modelo;
- temperatura e limite de tokens;
- condição operacional ou experimental;
- parâmetros pedagógicos tipados.

As credenciais dos provedores não pertencem ao modelo. A configuração `extra="forbid"`
faz com que campos não declarados, incluindo `api_key`, sejam rejeitados. Isso reduz o
risco de uma credencial ser incluída nos registros experimentais.

## Parâmetros do plano de aula

`LessonPlanParameters` representa:

- objetivos de aprendizagem;
- duração;
- metodologia;
- materiais e recursos;
- estratégia de avaliação;
- fluxo da aula;
- diferenciação e adaptações.

Tema e nível educacional pertencem ao `GenerationRequest`. Juntos aos cinco primeiros
campos acima, formam os sete requisitos do protocolo experimental.

Fluxo da aula e diferenciação continuam disponíveis para o modo operacional, mas não
integram os sete requisitos usados inicialmente na comparação C0-C1-C2.

## Condições de geração

- `operational`: uso normal da aplicação.
- `c0_generic`: solicitação genérica com tema e tipo de material.
- `c1_free_text`: as sete informações apresentadas como texto livre.
- `c2_structured`: as mesmas sete informações transformadas em instrução estruturada.

C1 e C2 exigem a presença dos sete requisitos. C0 aceita a ausência dos parâmetros que
não serão enviados no prompt genérico.

## Escopo desta etapa

O contrato inicial aceita somente `lesson_plan`. Essa restrição é intencional porque o
plano de aula é o primeiro objeto da avaliação computacional. Modelos tipados para notas
de aula, listas de exercícios e mapas mentais serão adicionados antes da migração desses
módulos.

## Exemplo

```python
from models import (
    DocumentType,
    GenerationRequest,
    LessonPlanParameters,
    Provider,
)

request = GenerationRequest(
    document_type=DocumentType.LESSON_PLAN,
    subject="Ciências",
    topic="Ciclo da água",
    grade_level="6º ano",
    language="pt-BR",
    provider=Provider.GOOGLE,
    model="gemini-model-id",
    pedagogical_parameters=LessonPlanParameters(
        learning_objectives="Compreender as etapas do ciclo da água",
        duration_minutes=50,
        methodology="Aprendizagem baseada em problemas",
        materials="Quadro, projetor e fichas",
        assessment_strategy="Avaliação formativa",
    ),
)
```

O conteúdo pode ser serializado com `request.model_dump_json()`. Nas próximas etapas,
essa representação será usada pela construção dos prompts e pelo registro das execuções.

## Verificação

Execute, na raiz do projeto:

```powershell
python -m unittest discover -s tests -v
```

Os testes verificam serialização, campos experimentais obrigatórios, normalização de
texto, comportamento de C0 e rejeição de credenciais.

## Migração incremental do plano de aula

O plano de aula já utiliza as duas primeiras camadas novas:

1. `pedagogical.lesson_plan_request_from_form` converte os dados temporariamente
   recebidos da interface atual em `GenerationRequest`;
2. `prompting.build_lesson_plan_prompt` recebe apenas o modelo validado e produz um
   `PromptArtifact` imutável, versionado e identificado por SHA-256;
3. o gerador envia o texto desse artefato ao manipulador de LLM já existente.

O antigo construtor de prompt foi removido do gerador para não manter duas fontes de
regras. O adaptador de formulário é transitório e será removido quando a camada de
apresentação passar a construir `GenerationRequest` diretamente.

O idioma agora é um parâmetro explícito da solicitação e uma instrução explícita do
prompt, em vez de ser inferido a partir da disciplina ou do tópico.

O próximo marco é substituir o manipulador central por adaptadores de provedor que
implementem uma interface comum e retornem metadados padronizados.

## Camada de integração Multi-LLM

O marco seguinte introduziu `ProviderGateway` e quatro adaptadores independentes:

- `OpenAIAdapter`;
- `GoogleAdapter`;
- `HuggingFaceAdapter`;
- `OllamaAdapter`.

Todos recebem `GenerationRequest` e `PromptArtifact` e devolvem `ProviderResponse`.
Essa resposta comum preserva conteúdo, provedor, modelo, latência, tokens quando
disponíveis, motivo de finalização e parâmetros efetivamente enviados. As credenciais
continuam restritas ao argumento transitório `connection_config` e nunca são copiadas
para a resposta.

Os quatro módulos utilizam o gateway. O antigo `api_handler.py` foi removido após a
migração da última dependência pertencente ao escopo da arquitetura.

## Processamento e registro reprodutível

A resposta bruta passa por `processing.process_response`, que produz uma versão limpa
sem sobrescrever o conteúdo original. A limpeza é deliberadamente conservadora e, nesta
etapa, remove apenas blocos técnicos `<think>` e excesso de linhas vazias.

Cada tentativa de plano de aula gera um `ExecutionRecord` no formato JSONL, incluindo:

- solicitação canônica e condição de geração;
- texto, versão e hash do prompt;
- provedor, modelo, parâmetros, latência e tokens disponíveis;
- resposta bruta e processada;
- avisos de processamento, status e erro, quando houver.

Os registros locais são gravados em `data/executions.jsonl`. Esse arquivo e seu lock são
ignorados pelo Git porque podem crescer rapidamente e conter entradas fornecidas pelo
professor. Para os experimentos, os registros deverão ser copiados para um diretório de
execução identificado e acompanhado do respectivo manifesto.

## Exportação independente

A exportação do plano de aula foi retirada do gerador e movida para
`exporters.lesson_plan_docx`. O exportador recebe apenas o conteúdo processado e o
`GenerationRequest`; portanto, pode recriar o documento a partir de uma execução
armazenada sem fazer uma nova chamada ao modelo.

O subconjunto de Markdown compartilhado está isolado em `exporters.markdown_docx` e
converte títulos, listas, itens numerados e parágrafos. O gerador do plano de aula não
contém mais regras de Word nem imports de `python-docx`.
