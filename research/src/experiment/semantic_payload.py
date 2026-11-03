"""Canonical semantic input shared by experimental conditions C1 and C2."""

from hashlib import sha256
import json

from pydantic import BaseModel, ConfigDict, Field

from models import DocumentType, GenerationRequest, LessonPlanParameters


class LessonPlanSemanticPayload(BaseModel):
    """Exactly the seven requirements controlled by the experiment.

    C1 and C2 must always be rendered from the same instance of this model.
    Operational fields such as lesson flow and differentiation are deliberately
    absent and rejected if supplied directly.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    topic: str = Field(min_length=1)
    grade_level: str = Field(min_length=1)
    learning_objectives: str = Field(min_length=1)
    duration_minutes: int = Field(ge=10)
    methodology: str = Field(min_length=1)
    materials: str = Field(min_length=1)
    assessment_strategy: str = Field(min_length=1)

    @classmethod
    def from_request(cls, request: GenerationRequest) -> "LessonPlanSemanticPayload":
        """Extract only experimental information from a validated lesson plan."""

        if request.document_type is not DocumentType.LESSON_PLAN:
            raise ValueError("The experimental payload supports only lesson_plan")
        parameters = request.pedagogical_parameters
        if not isinstance(parameters, LessonPlanParameters):
            raise ValueError("LessonPlanParameters are required")

        missing = parameters.missing_experimental_requirements()
        if missing:
            raise ValueError(
                "The seven experimental requirements must be complete; missing: "
                + ", ".join(missing)
            )

        return cls(
            topic=request.topic,
            grade_level=request.grade_level,
            learning_objectives=parameters.learning_objectives,
            duration_minutes=parameters.duration_minutes,
            methodology=parameters.methodology,
            materials=parameters.materials,
            assessment_strategy=parameters.assessment_strategy,
        )

    def canonical_json(self) -> str:
        """Return a stable serialization used to prove common semantic input."""

        return json.dumps(
            self.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    @property
    def semantic_hash(self) -> str:
        """Identify the exact seven-requirement payload independently of layout."""

        return sha256(self.canonical_json().encode("utf-8")).hexdigest()
