"""Word export for a processed lesson plan."""

from exporters.standard_docx import export_standard_docx
from models import GenerationRequest


def export_lesson_plan_docx(content: str, request: GenerationRequest) -> bytes:
    """Create a DOCX without invoking an LLM or reading presentation state."""

    if not content or not content.strip():
        raise ValueError("Cannot export an empty lesson plan")

    portuguese = request.language.lower().startswith("pt")
    duration_label = "Duração" if portuguese else "Duration"
    minutes_label = "minutos" if portuguese else "minutes"

    duration = request.pedagogical_parameters.duration_minutes
    metadata = [f"{duration_label}: {duration} {minutes_label}"] if duration is not None else []
    return export_standard_docx(
        content,
        request,
        document_label_pt="Plano de Aula",
        document_label_en="Lesson Plan",
        metadata=metadata,
    )
