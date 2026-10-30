"""Mind-map adapter for the shared generation pipeline."""

from application import execute_generation
from exporters import export_mind_map_docx
from pedagogical import mind_map_request_from_form
from prompting import build_mind_map_prompt


def generate_mind_map(params):
    request = mind_map_request_from_form(params)
    prompt = build_mind_map_prompt(request)
    return execute_generation(request, prompt, params["llm_config"], export_mind_map_docx).as_legacy_dict()
