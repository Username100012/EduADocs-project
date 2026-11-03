"""Versioned prompts for notes, exercises and mind maps."""

from models import GenerationRequest
from prompting.models import PromptArtifact


def _boolean(value: bool, pt: bool) -> str:
    return ("Sim" if value else "Não") if pt else ("Yes" if value else "No")


def build_lecture_notes_prompt(request: GenerationRequest) -> PromptArtifact:
    p = request.pedagogical_parameters
    pt = request.language.lower().startswith("pt")
    text = (
        f"""Crie notas de aula para {request.subject}, nível {request.grade_level}.
Tópico: {request.topic}
Idioma: {request.language}
Nível de detalhe: {p.detail_level}
Formato: {p.format_style}
Incluir exemplos: {_boolean(p.include_examples, pt)}
Incluir referências: {_boolean(p.include_references, pt)}

Organize em introdução e objetivos, conceitos e definições, explicações, exemplos quando solicitados, síntese e referências quando solicitadas. Use títulos Markdown e produza todo o conteúdo em português."""
        if pt else
        f"""Create lecture notes for {request.subject} at {request.grade_level} level.
Topic: {request.topic}
Language: {request.language}
Detail level: {p.detail_level}
Format: {p.format_style}
Include examples: {_boolean(p.include_examples, pt)}
Include references: {_boolean(p.include_references, pt)}

Organize into introduction and goals, concepts and definitions, explanations, requested examples, summary, and requested references. Use Markdown headings and write in English."""
    )
    return PromptArtifact(text, "lecture-notes-operational-v1.0.0", ("topic", "grade_level", "detail_level", "format_style"))


def build_exercise_list_prompt(request: GenerationRequest) -> PromptArtifact:
    p = request.pedagogical_parameters
    pt = request.language.lower().startswith("pt")
    types = ", ".join(p.question_types)
    text = (
        f"""Crie uma lista de exercícios para {request.subject}, nível {request.grade_level}.
Tópico: {request.topic}
Idioma: {request.language}
Número de questões: {p.num_questions}
Dificuldade: {p.difficulty}
Tipos de questões: {types}
Incluir gabarito ou soluções: {_boolean(p.include_answer_key, pt)}

Use exatamente a quantidade solicitada, instruções claras, numeração sequencial e títulos Markdown. Inclua o gabarito somente quando solicitado. Produza todo o conteúdo em português."""
        if pt else
        f"""Create an exercise list for {request.subject} at {request.grade_level} level.
Topic: {request.topic}
Language: {request.language}
Number of questions: {p.num_questions}
Difficulty: {p.difficulty}
Question types: {types}
Include answer key or solutions: {_boolean(p.include_answer_key, pt)}

Use exactly the requested number, clear instructions, sequential numbering and Markdown headings. Include the answer key only when requested. Write in English."""
    )
    return PromptArtifact(text, "exercise-list-operational-v1.0.0", ("topic", "grade_level", "num_questions", "difficulty", "question_types", "include_answer_key"))


def build_mind_map_prompt(request: GenerationRequest) -> PromptArtifact:
    p = request.pedagogical_parameters
    pt = request.language.lower().startswith("pt")
    text = (
        f"""Crie um mapa mental textual para {request.subject}, nível {request.grade_level}.
Tópico central: {request.topic}
Idioma: {request.language}
Ramos principais: {p.main_branches}
Níveis de profundidade: {p.depth_levels}
Incluir exemplos: {_boolean(p.include_examples, pt)}
Destacar hierarquia: {_boolean(p.highlight_hierarchy, pt)}

Use um único H1 para o tópico central, H2 para cada ramo e listas aninhadas com dois espaços por nível. Mantenha cada nó curto e produza todo o conteúdo em português."""
        if pt else
        f"""Create a textual mind map for {request.subject} at {request.grade_level} level.
Central topic: {request.topic}
Language: {request.language}
Main branches: {p.main_branches}
Depth levels: {p.depth_levels}
Include examples: {_boolean(p.include_examples, pt)}
Emphasize hierarchy: {_boolean(p.highlight_hierarchy, pt)}

Use one H1 for the central topic, H2 for each branch, and nested lists with two spaces per level. Keep nodes short and write in English."""
    )
    return PromptArtifact(text, "mind-map-operational-v1.0.0", ("topic", "grade_level", "main_branches", "depth_levels", "include_examples", "highlight_hierarchy"))
