"""Thin DOCX configurations for notes, exercises and mind maps."""

from exporters.standard_docx import export_standard_docx
from models import GenerationRequest


def export_lecture_notes_docx(content: str, request: GenerationRequest) -> bytes:
    return export_standard_docx(content, request, document_label_pt="Notas de Aula", document_label_en="Lecture Notes")


def export_exercise_list_docx(content: str, request: GenerationRequest) -> bytes:
    p = request.pedagogical_parameters
    pt = request.language.lower().startswith("pt")
    metadata = [
        f"{'Quantidade de questões' if pt else 'Number of questions'}: {p.num_questions}",
        f"{'Dificuldade' if pt else 'Difficulty'}: {p.difficulty}",
    ]
    return export_standard_docx(content, request, document_label_pt="Lista de Exercícios", document_label_en="Exercise List", metadata=metadata)


def export_mind_map_docx(content: str, request: GenerationRequest) -> bytes:
    return export_standard_docx(content, request, document_label_pt="Mapa Mental", document_label_en="Mind Map")
