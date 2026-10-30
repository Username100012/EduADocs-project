"""Provider-independent input models for educational material generation.

These models represent the boundary between the presentation layer and the
pedagogical parameterization layer. They intentionally do not contain API keys
or any provider-specific client objects.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


NonEmptyText = Annotated[str, Field(min_length=1)]


class DocumentType(str, Enum):
    """Educational artifacts currently supported by EduADocs."""

    LESSON_PLAN = "lesson_plan"
    LECTURE_NOTES = "lecture_notes"
    EXERCISE_LIST = "exercise_list"
    MIND_MAP = "mind_map"


class ExperimentalCondition(str, Enum):
    """Generation modes used by the application and computational study."""

    OPERATIONAL = "operational"
    C0_GENERIC = "c0_generic"
    C1_FREE_TEXT = "c1_free_text"
    C2_STRUCTURED = "c2_structured"


class Provider(str, Enum):
    """LLM providers represented by the Multi-LLM integration layer."""

    OPENAI = "openai"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"


class StrictModel(BaseModel):
    """Base configuration that rejects undeclared architectural fields."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
    )


class LessonPlanParameters(StrictModel):
    """Pedagogical parameters used by the lesson-plan module.

    The five optional fields at the beginning complement ``topic`` and
    ``grade_level`` from :class:`GenerationRequest`, forming the seven
    requirements evaluated in conditions C1 and C2.

    ``lesson_flow`` and ``include_differentiation`` belong to the operational
    application. They are not part of the seven requirements in the current
    experimental protocol.
    """

    learning_objectives: str | None = None
    duration_minutes: int | None = Field(default=None, ge=10)
    methodology: str | None = None
    materials: str | None = None
    assessment_strategy: str | None = None
    lesson_flow: str | None = None
    include_differentiation: bool = False

    @field_validator(
        "learning_objectives",
        "methodology",
        "materials",
        "assessment_strategy",
        "lesson_flow",
        mode="before",
    )
    @classmethod
    def empty_text_becomes_none(cls, value: object) -> object:
        """Normalize blank optional fields so absence has one representation."""

        if isinstance(value, str) and not value.strip():
            return None
        return value

    def missing_experimental_requirements(self) -> list[str]:
        """Return missing lesson-plan requirements for C1/C2 validation."""

        required = {
            "learning_objectives": self.learning_objectives,
            "duration_minutes": self.duration_minutes,
            "methodology": self.methodology,
            "materials": self.materials,
            "assessment_strategy": self.assessment_strategy,
        }
        return [name for name, value in required.items() if value is None]


class LectureNotesParameters(StrictModel):
    """Parameters that control lecture-note depth and presentation."""

    detail_level: NonEmptyText
    format_style: NonEmptyText
    include_examples: bool = True
    include_references: bool = False


class ExerciseListParameters(StrictModel):
    """Parameters that control an exercise list."""

    num_questions: int = Field(ge=1)
    difficulty: NonEmptyText
    question_types: list[NonEmptyText] = Field(min_length=1)
    include_answer_key: bool = True


class MindMapParameters(StrictModel):
    """Parameters that control the hierarchical mind-map representation."""

    main_branches: int = Field(ge=3)
    depth_levels: int = Field(ge=2, le=6)
    include_examples: bool = True
    highlight_hierarchy: bool = True


PedagogicalParameters = (
    LessonPlanParameters
    | LectureNotesParameters
    | ExerciseListParameters
    | MindMapParameters
)


class GenerationRequest(StrictModel):
    """Canonical, provider-independent request passed between architecture layers.

    API credentials are deliberately excluded. They remain in the provider
    configuration layer and must never be serialized with experimental data.
    """

    execution_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    document_type: DocumentType
    subject: NonEmptyText
    topic: NonEmptyText
    grade_level: NonEmptyText
    language: NonEmptyText = "pt-BR"
    provider: Provider
    model: NonEmptyText
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, gt=0)
    experimental_condition: ExperimentalCondition = ExperimentalCondition.OPERATIONAL
    pedagogical_parameters: PedagogicalParameters

    @model_validator(mode="after")
    def validate_document_parameters(self) -> "GenerationRequest":
        """Ensure each material is paired with its own parameter model."""

        expected_types = {
            DocumentType.LESSON_PLAN: LessonPlanParameters,
            DocumentType.LECTURE_NOTES: LectureNotesParameters,
            DocumentType.EXERCISE_LIST: ExerciseListParameters,
            DocumentType.MIND_MAP: MindMapParameters,
        }
        expected = expected_types[self.document_type]
        if not isinstance(self.pedagogical_parameters, expected):
            raise ValueError(
                f"{self.document_type.value} requires {expected.__name__}"
            )

        if self.experimental_condition in {
            ExperimentalCondition.C1_FREE_TEXT,
            ExperimentalCondition.C2_STRUCTURED,
        }:
            if self.document_type is not DocumentType.LESSON_PLAN:
                raise ValueError("C1 and C2 currently support only lesson_plan")
            missing = self.pedagogical_parameters.missing_experimental_requirements()
            if missing:
                raise ValueError(
                    "C1 and C2 require all seven experimental requirements; "
                    "missing lesson-plan fields: " + ", ".join(missing)
                )
        return self
