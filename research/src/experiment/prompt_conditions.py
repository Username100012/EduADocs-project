"""Versioned prompt builders for the computational experiment conditions."""

from prompting import PromptArtifact
from experiment.semantic_payload import LessonPlanSemanticPayload


C0_PROMPT_VERSION = "lesson-plan-c0-generic-v1.0.0"
C1_PROMPT_VERSION = "lesson-plan-c1-free-text-v1.0.0"
C2_PROMPT_VERSION = "lesson-plan-c2-structured-v1.0.0"

EXPERIMENTAL_REQUIREMENTS = (
    "topic",
    "grade_level",
    "learning_objectives",
    "duration_minutes",
    "methodology",
    "materials",
    "assessment_strategy",
)


def build_c0_prompt(topic: str) -> PromptArtifact:
    """Build the generic condition using only material type and topic.

    The deliberately narrow signature prevents the other six controlled
    requirements and operational parameters from entering condition C0.
    """

    normalized_topic = topic.strip()
    if not normalized_topic:
        raise ValueError("C0 requires a non-empty topic")

    return PromptArtifact(
        text=f"Elabore um plano de aula sobre o tema: {normalized_topic}.",
        template_version=C0_PROMPT_VERSION,
        expected_requirements=("topic",),
    )


def build_c1_prompt(payload: LessonPlanSemanticPayload) -> PromptArtifact:
    """Render all seven requirements as one free-form natural-language request."""

    text = (
        f"Elabore um plano de aula sobre {payload.topic} para estudantes do nível "
        f"{payload.grade_level}, com duração de {payload.duration_minutes} minutos. "
        f"O objetivo de aprendizagem é {payload.learning_objectives}. Utilize "
        f"{payload.methodology} como metodologia, considerando {payload.materials} "
        f"como materiais e recursos disponíveis e {payload.assessment_strategy} "
        f"como estratégia de avaliação."
    )
    return PromptArtifact(
        text=text,
        template_version=C1_PROMPT_VERSION,
        expected_requirements=EXPERIMENTAL_REQUIREMENTS,
        semantic_payload_hash=payload.semantic_hash,
    )


def build_c2_prompt(payload: LessonPlanSemanticPayload) -> PromptArtifact:
    """Render the same seven requirements as an explicitly structured request."""

    text = f"""TAREFA
Elaborar um plano de aula.

PARÂMETROS PEDAGÓGICOS
- Tópico: {payload.topic}
- Nível educacional: {payload.grade_level}
- Objetivo de aprendizagem: {payload.learning_objectives}
- Duração: {payload.duration_minutes} minutos
- Metodologia: {payload.methodology}
- Materiais e recursos: {payload.materials}
- Estratégia de avaliação: {payload.assessment_strategy}

INSTRUÇÃO DE SAÍDA
Produza o plano de aula respeitando todos os parâmetros pedagógicos apresentados."""
    return PromptArtifact(
        text=text,
        template_version=C2_PROMPT_VERSION,
        expected_requirements=EXPERIMENTAL_REQUIREMENTS,
        semantic_payload_hash=payload.semantic_hash,
    )
