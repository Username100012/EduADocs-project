"""Translate lesson-plan form data into the canonical domain model."""

from collections.abc import Mapping
from typing import Any

from models import (
    DocumentType,
    ExperimentalCondition,
    GenerationRequest,
    LessonPlanParameters,
)
from pedagogical.common import common_request_fields


def lesson_plan_request_from_form(
    form_data: Mapping[str, Any],
    *,
    condition: ExperimentalCondition = ExperimentalCondition.OPERATIONAL,
) -> GenerationRequest:
    """Create a validated request without depending on Streamlit.

    ``form_data`` is retained only as an adapter for the current interface. The
    resulting object is the sole input expected by the new architecture layers.
    Provider credentials are read neither here nor by the domain model.
    """

    return GenerationRequest(
        **common_request_fields(form_data),
        document_type=DocumentType.LESSON_PLAN,
        experimental_condition=condition,
        pedagogical_parameters=LessonPlanParameters(
            learning_objectives=form_data.get("learning_objectives"),
            duration_minutes=form_data.get("duration_minutes"),
            methodology=form_data.get("methodology"),
            materials=form_data.get("materials"),
            assessment_strategy=form_data.get("assessment_strategy"),
            lesson_flow=form_data.get("lesson_flow"),
            include_differentiation=form_data.get("include_differentiation", False),
        ),
    )
