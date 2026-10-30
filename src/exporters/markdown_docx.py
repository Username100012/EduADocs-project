"""Small, deterministic Markdown subset used by DOCX exporters."""

import re

from docx.document import Document as DocumentObject


def add_markdown_content(document: DocumentObject, content: str) -> None:
    """Append supported Markdown blocks to an existing Word document.

    The generated prompts request only headings, bullets, numbered items and
    paragraphs. Unsupported Markdown is intentionally treated as plain text.
    """

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            document.add_paragraph("")
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            document.add_heading(_plain_text(heading.group(2)), level=len(heading.group(1)))
            continue

        bullet = re.match(r"^[-*•]\s+(.+)$", line)
        if bullet:
            document.add_paragraph(_plain_text(bullet.group(1)), style="List Bullet")
            continue

        numbered = re.match(r"^\d+[.)]\s+(.+)$", line)
        if numbered:
            document.add_paragraph(_plain_text(numbered.group(1)), style="List Number")
            continue

        document.add_paragraph(_plain_text(line))


def _plain_text(text: str) -> str:
    """Remove the inline emphasis syntax currently emitted by the prompts."""

    return re.sub(r"\*\*(.*?)\*\*", r"\1", text)
