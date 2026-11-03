"""Versioned prompt construction for the lesson-plan module."""

from models import DocumentType, GenerationRequest
from prompting.models import PromptArtifact


LESSON_PLAN_PROMPT_VERSION = "lesson-plan-operational-v1.0.0"
LESSON_PLAN_REQUIREMENTS = (
    "topic",
    "grade_level",
    "learning_objectives",
    "duration_minutes",
    "methodology",
    "materials",
    "assessment_strategy",
)


def _display(value: object | None, language: str) -> str:
    if value is None:
        return "Não informado" if language.lower().startswith("pt") else "Not specified"
    return str(value)


def build_lesson_plan_prompt(request: GenerationRequest) -> PromptArtifact:
    """Build a deterministic prompt from validated pedagogical parameters."""

    if request.document_type is not DocumentType.LESSON_PLAN:
        raise ValueError("Lesson-plan prompt builder received another document type")

    parameters = request.pedagogical_parameters
    portuguese = request.language.lower().startswith("pt")
    yes = "Sim" if portuguese else "Yes"
    no = "Não" if portuguese else "No"
    differentiation = yes if parameters.include_differentiation else no

    if portuguese:
        text = f"""Crie um plano de aula detalhado para a disciplina {request.subject}, no nível {request.grade_level}.

Tópico: {request.topic}
Idioma da resposta: {request.language}
Duração: {_display(parameters.duration_minutes, request.language)} minutos
Objetivos de aprendizagem: {_display(parameters.learning_objectives, request.language)}
Materiais e recursos: {_display(parameters.materials, request.language)}
Metodologia de ensino: {_display(parameters.methodology, request.language)}
Estratégia de avaliação: {_display(parameters.assessment_strategy, request.language)}
Fluxo da aula: {_display(parameters.lesson_flow, request.language)}
Incluir diferenciação ou adaptações: {differentiation}

Organize o plano com as seguintes seções:
1. Título e objetivos da aula
2. Conhecimentos prévios ou pré-requisitos
3. Fluxo da aula passo a passo, usando o fluxo informado quando disponível
4. Materiais e recursos
5. Estratégia de avaliação
6. Diferenciação ou adaptações, quando solicitadas
7. Atividades de extensão, quando pertinentes

Regras de formatação:
- Use títulos Markdown (#, ## e ###).
- Use listas com marcadores para atividades e enumerações.
- Mantenha títulos consistentes e não use linhas horizontais.
- Produza todo o conteúdo em português."""
    else:
        text = f"""Create a detailed lesson plan for {request.subject} at {request.grade_level} level.

Topic: {request.topic}
Response language: {request.language}
Duration: {_display(parameters.duration_minutes, request.language)} minutes
Learning objectives: {_display(parameters.learning_objectives, request.language)}
Materials and resources: {_display(parameters.materials, request.language)}
Teaching methodology: {_display(parameters.methodology, request.language)}
Assessment strategy: {_display(parameters.assessment_strategy, request.language)}
Lesson flow: {_display(parameters.lesson_flow, request.language)}
Include differentiation or adaptations: {differentiation}

Organize the plan with these sections:
1. Lesson title and objectives
2. Prior knowledge or prerequisites
3. Step-by-step lesson flow, using the supplied flow when available
4. Materials and resources
5. Assessment strategy
6. Differentiation or adaptations, when requested
7. Extension activities, when appropriate

Formatting rules:
- Use Markdown headings (#, ## and ###).
- Use bullet points for activities and lists.
- Keep headings consistent and do not use horizontal rules.
- Produce all content in English."""

    return PromptArtifact(
        text=text,
        template_version=LESSON_PLAN_PROMPT_VERSION,
        expected_requirements=LESSON_PLAN_REQUIREMENTS,
    )
