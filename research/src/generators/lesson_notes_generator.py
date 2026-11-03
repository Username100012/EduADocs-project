"""Lecture-notes adapter for the shared generation pipeline."""

from application import execute_generation
from exporters import export_lecture_notes_docx
from pedagogical import lecture_notes_request_from_form
from prompting import build_lecture_notes_prompt


def generate_lecture_notes(params):
    request = lecture_notes_request_from_form(params)
    prompt = build_lecture_notes_prompt(request)
    return execute_generation(request, prompt, params["llm_config"], export_lecture_notes_docx).as_legacy_dict()
