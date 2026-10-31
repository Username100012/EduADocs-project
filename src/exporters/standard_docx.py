"""Shared DOCX shell for educational materials represented as Markdown."""

import io
from collections.abc import Iterable

from docx import Document
from docx.shared import Cm, Pt
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
    for section in document.sections:
        section.top_margin = section.bottom_margin = Cm(1.8)
        section.left_margin = section.right_margin = Cm(2)
    normal = document.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.line_spacing = 1.08
    for name in ['List Bullet', 'List Bullet 2', 'List Bullet 3', 'List Number', 'List Number 2', 'List Number 3']:
        document.styles[name].paragraph_format.space_after = Pt(3)
    for level, size in [(1, 15), (2, 13), (3, 12)]:
        style = document.styles[f'Heading {level}']
        style.font.size = Pt(size)
        style.paragraph_format.space_before = Pt(9)
        style.paragraph_format.space_after = Pt(4)
    title = document.add_heading(f"{request.subject} — {label}", 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    document.add_paragraph(f"{topic}: {request.topic}")
    document.add_paragraph(f"{grade}: {request.grade_level}")
    for item in metadata:
        document.add_paragraph(item)
    add_markdown_content(document, content)
    output = io.BytesIO()
    document.save(output)
    return output.getvalue()
