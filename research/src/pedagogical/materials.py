"""Typed parameterization adapters for the remaining educational materials."""

from collections.abc import Mapping
from typing import Any

from models import (
    DocumentType,
    ExerciseListParameters,
    GenerationRequest,
    LectureNotesParameters,
    MindMapParameters,
)
from pedagogical.common import common_request_fields


def lecture_notes_request_from_form(data: Mapping[str, Any]) -> GenerationRequest:
    return GenerationRequest(
        **common_request_fields(data),
        document_type=DocumentType.LECTURE_NOTES,
        pedagogical_parameters=LectureNotesParameters(
            detail_level=data.get("detail_level") or "Standard",
            format_style=data.get("format_style") or "Paragraphs",
            include_examples=data.get("include_examples", True),
            include_references=data.get("include_references", False),
        ),
    )


def exercise_list_request_from_form(data: Mapping[str, Any]) -> GenerationRequest:
    return GenerationRequest(
        **common_request_fields(data),
        document_type=DocumentType.EXERCISE_LIST,
        pedagogical_parameters=ExerciseListParameters(
            num_questions=data.get("num_questions", 10),
            difficulty=data.get("difficulty") or "Medium",
            question_types=data.get("question_types") or ["Short Answer"],
            include_answer_key=data.get("include_answer_key", True),
        ),
    )


def mind_map_request_from_form(data: Mapping[str, Any]) -> GenerationRequest:
    return GenerationRequest(
        **common_request_fields(data),
        document_type=DocumentType.MIND_MAP,
        pedagogical_parameters=MindMapParameters(
            main_branches=data.get("main_branches", 6),
            depth_levels=data.get("depth_levels", 3),
            include_examples=data.get("include_examples", True),
            highlight_hierarchy=data.get("highlight_hierarchy", True),
        ),
    )
