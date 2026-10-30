"""Domain models shared by the EduADocs architecture layers."""

from .generation_request import (
    DocumentType,
    ExperimentalCondition,
    ExerciseListParameters,
    GenerationRequest,
    LessonPlanParameters,
    LectureNotesParameters,
    MindMapParameters,
    Provider,
)

__all__ = [
    "DocumentType",
    "ExperimentalCondition",
    "ExerciseListParameters",
    "GenerationRequest",
    "LessonPlanParameters",
    "LectureNotesParameters",
    "MindMapParameters",
    "Provider",
]
