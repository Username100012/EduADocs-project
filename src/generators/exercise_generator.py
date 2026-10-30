"""Exercise-list adapter for the shared generation pipeline."""

from application import execute_generation
from exporters import export_exercise_list_docx
from pedagogical import exercise_list_request_from_form
from prompting import build_exercise_list_prompt


def generate_exercises(params):
    request = exercise_list_request_from_form(params)
    prompt = build_exercise_list_prompt(request)
    return execute_generation(request, prompt, params["llm_config"], export_exercise_list_docx).as_legacy_dict()
