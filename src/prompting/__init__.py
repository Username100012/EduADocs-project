"""Versioned, provider-independent prompt construction."""

from .lesson_plan import LESSON_PLAN_PROMPT_VERSION, build_lesson_plan_prompt
from .models import PromptArtifact
from .materials import (
    build_exercise_list_prompt,
    build_lecture_notes_prompt,
    build_mind_map_prompt,
)

__all__ = [
    "LESSON_PLAN_PROMPT_VERSION",
    "PromptArtifact",
    "build_lesson_plan_prompt",
    "build_exercise_list_prompt",
    "build_lecture_notes_prompt",
    "build_mind_map_prompt",
]
