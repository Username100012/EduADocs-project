from application import execute_generation
from exporters import export_lesson_plan_docx
from pedagogical import lesson_plan_request_from_form
from prompting import build_lesson_plan_prompt


def generate_lesson_plan(params):
    """Adapt the current UI payload to the shared architecture pipeline."""

    request = lesson_plan_request_from_form(params)
    prompt_artifact = build_lesson_plan_prompt(request)
    return execute_generation(
        request,
        prompt_artifact,
        params["llm_config"],
        export_lesson_plan_docx,
    ).as_legacy_dict()
