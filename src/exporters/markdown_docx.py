"""Markdown paragraphs, nested lists and native Word math for DOCX output."""
import re
from docx.oxml import parse_xml
from docx.shared import Cm

MATH = re.compile(r'\$\$(.+?)\$\$|\\\[(.+?)\\\]|\\\((.+?)\\\)|(?<![\\$])\$(?!\$)(.+?)(?<!\\)\$', re.S)
INLINE = re.compile(r'(\*\*.*?\*\*|`[^`]+`)')


def _inline(paragraph, text):
    for part in INLINE.split(text):
        if not part:
            continue
        run = paragraph.add_run(part[2:-2] if part.startswith('**') and part.endswith('**') else part[1:-1] if part.startswith('`') and part.endswith('`') else part)
        run.bold = part.startswith('**') and part.endswith('**')


def _math(paragraph, expression):
    from latex2mathml.converter import convert
    from mathml2omml import convert as to_omml
    try:
        xml = to_omml(convert(expression.strip()))
        xml = xml.replace('<m:oMath>', '<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">', 1)
        paragraph._p.append(parse_xml(xml))
    except Exception as exc:
        # Do not silently export literal TeX while claiming successful rendering.
        raise ValueError('Não foi possível converter uma expressão matemática para Word: ' + expression[:100]) from exc


def add_inline_content(paragraph, text):
    cursor = 0
    for match in MATH.finditer(text):
        _inline(paragraph, text[cursor:match.start()])
        _math(paragraph, next(group for group in match.groups() if group is not None))
        cursor = match.end()
    _inline(paragraph, text[cursor:])


def add_markdown_content(document, content):
    # Keep display expressions intact even if they span several Markdown lines.
    content = re.sub(r'\$\$(.+?)\$\$|\\\[(.+?)\\\]', lambda m: '$$' + next(g for g in m.groups() if g is not None).replace('\n', ' ') + '$$', content, flags=re.S)
    indents = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or re.fullmatch(r'(?:---+|\*\*\*+|___+)', line):
            continue
        heading = re.match(r'^(#{1,4})\s+(.+)$', line)
        if heading:
            p = document.add_heading('', level=min(len(heading[1]), 3))
            add_inline_content(p, heading[2]); indents = []
            continue
        item = re.match(r'^(\s*)([-*•]|\d+[.)])\s+(.+)$', raw_line.expandtabs(4))
        if item:
            indent = len(item[1])
            while indents and indent < indents[-1]:
                indents.pop()
            if not indents or indent > indents[-1]:
                indents.append(indent)
            depth = min(len(indents)-1, 2)
            base = 'List Bullet' if item[2] in '-*•' else 'List Number'
            style = base + (f' {depth+1}' if depth else '')
            p = document.add_paragraph(style=style)
            p.paragraph_format.left_indent = Cm(0.65 + depth*0.6)
            p.paragraph_format.first_line_indent = Cm(-0.3)
            add_inline_content(p, item[3])
        else:
            p = document.add_paragraph()
            add_inline_content(p, line)
        p.paragraph_format.keep_with_next = False
        p.paragraph_format.keep_together = False
