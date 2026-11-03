"""Shared DOCX shell for educational materials represented as Markdown."""

import io
from collections.abc import Iterable

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from exporters.markdown_docx import add_markdown_content
from models import GenerationRequest


def export_standard_docx(
    content: str,
    request: GenerationRequest,
    *,
    document_label_pt: str,
    document_label_en: str,
    metadata: Iterable[str] = (),
) -> bytes:
    if not content or not content.strip():
        raise ValueError("Cannot export empty content")
    pt = request.language.lower().startswith("pt")
    label = document_label_pt if pt else document_label_en
    topic = "Tópico" if pt else "Topic"
    grade = "Nível de ensino" if pt else "Grade level"
    document = Document()
    title = document.add_heading(f"{request.subject} — {label}", 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    document.add_heading(f"{topic}: {request.topic}", level=2)
    document.add_heading(f"{grade}: {request.grade_level}", level=3)
    for item in metadata:
        document.add_paragraph(item)
    add_markdown_content(document, content)
    output = io.BytesIO()
    document.save(output)
    return output.getvalue()
