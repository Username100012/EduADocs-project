import re

# Unicode characters that need LaTeX math-mode equivalents ($...$)
_UNICODE_MATH = [
    ('√', r'$\surd$'),
    ('±', r'$\pm$'),
    ('∓', r'$\mp$'),
    ('×', r'$\times$'),
    ('÷', r'$\div$'),
    ('≠', r'$\neq$'),
    ('≤', r'$\leq$'),
    ('≥', r'$\geq$'),
    ('≈', r'$\approx$'),
    ('≡', r'$\equiv$'),
    ('∝', r'$\propto$'),
    ('∞', r'$\infty$'),
    ('∑', r'$\sum$'),
    ('∏', r'$\prod$'),
    ('∫', r'$\int$'),
    ('∂', r'$\partial$'),
    ('∇', r'$\nabla$'),
    ('∈', r'$\in$'),
    ('∉', r'$\notin$'),
    ('⊂', r'$\subset$'),
    ('⊃', r'$\supset$'),
    ('∪', r'$\cup$'),
    ('∩', r'$\cap$'),
    ('∅', r'$\emptyset$'),
    ('→', r'$\rightarrow$'),
    ('←', r'$\leftarrow$'),
    ('↔', r'$\leftrightarrow$'),
    ('⇒', r'$\Rightarrow$'),
    ('⇐', r'$\Leftarrow$'),
    ('⇔', r'$\Leftrightarrow$'),
    ('α', r'$\alpha$'),
    ('β', r'$\beta$'),
    ('γ', r'$\gamma$'),
    ('δ', r'$\delta$'),
    ('ε', r'$\varepsilon$'),
    ('ζ', r'$\zeta$'),
    ('η', r'$\eta$'),
    ('θ', r'$\theta$'),
    ('λ', r'$\lambda$'),
    ('μ', r'$\mu$'),
    ('π', r'$\pi$'),
    ('ρ', r'$\rho$'),
    ('σ', r'$\sigma$'),
    ('τ', r'$\tau$'),
    ('φ', r'$\varphi$'),
    ('ω', r'$\omega$'),
    ('Δ', r'$\Delta$'),
    ('Σ', r'$\Sigma$'),
    ('Π', r'$\Pi$'),
    ('Ω', r'$\Omega$'),
    ('²', r'$^2$'),
    ('³', r'$^3$'),
    ('¹', r'$^1$'),
    ('⁰', r'$^0$'),
    ('⁴', r'$^4$'),
    ('⁵', r'$^5$'),
    ('⁶', r'$^6$'),
    ('⁷', r'$^7$'),
    ('⁸', r'$^8$'),
    ('⁹', r'$^9$'),
    ('₀', r'$_0$'),
    ('₁', r'$_1$'),
    ('₂', r'$_2$'),
    ('₃', r'$_3$'),
    ('₄', r'$_4$'),
    ('°', r'$^\circ$'),
    ('·', r'$\cdot$'),
]

# Unicode characters with direct text-mode equivalents
_UNICODE_TEXT = [
    ('—', r'---'),
    ('–', r'--'),
    (''', r"'"),
    (''', r"'"),
    ('"', r'``'),
    ('"', r"''"),
    ('…', r'\ldots{}'),
    ('«', r'\guillemotleft{}'),
    ('»', r'\guillemotright{}'),
    ('©', r'\textcopyright{}'),
    ('®', r'\textregistered{}'),
    ('™', r'\texttrademark{}'),
    ('§', r'\S{}'),
    ('¶', r'\P{}'),
    ('†', r'\dag{}'),
    ('‡', r'\ddag{}'),
    ('•', r'\textbullet{}'),
]


def _replace_unicode(text):
    """Replace Unicode symbols with LaTeX equivalents before escaping"""
    for char, replacement in _UNICODE_MATH:
        text = text.replace(char, replacement)
    for char, replacement in _UNICODE_TEXT:
        text = text.replace(char, replacement)
    return text


def _escape_latex(text):
    """Escape special LaTeX characters in plain text"""
    text = _replace_unicode(text)
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('#', r'\#'),
        ('^', r'\textasciicircum{}'),
        ('~', r'\textasciitilde{}'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
    ]
    # Protect already-inserted LaTeX commands from re-escaping
    # by splitting on them, escaping the plain parts only
    tokens = re.split(r'(\$[^$]*\$|\\[a-zA-Z]+\{[^}]*\}|\\[a-zA-Z]+\{\}|---?)', text)
    result = []
    for token in tokens:
        if re.match(r'\$[^$]*\$|\\[a-zA-Z]+\{[^}]*\}|\\[a-zA-Z]+\{\}|---?', token):
            result.append(token)
        else:
            for char, replacement in replacements:
                token = token.replace(char, replacement)
            result.append(token)
    return ''.join(result)


def _apply_inline_formatting(text):
    """Convert inline Markdown formatting to LaTeX commands"""
    # Bold+italic: ***text***
    text = re.sub(r'\*\*\*(.*?)\*\*\*', lambda m: r'\textbf{\textit{' + _escape_latex(m.group(1)) + '}}', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.*?)\*\*', lambda m: r'\textbf{' + _escape_latex(m.group(1)) + '}', text)
    # Italic: *text* or _text_
    text = re.sub(r'\*(.*?)\*', lambda m: r'\textit{' + _escape_latex(m.group(1)) + '}', text)
    text = re.sub(r'(?<!\w)_(.*?)_(?!\w)', lambda m: r'\textit{' + _escape_latex(m.group(1)) + '}', text)
    # Inline code: `code`
    text = re.sub(r'`(.*?)`', lambda m: r'\texttt{' + _escape_latex(m.group(1)) + '}', text)
    return text


def _process_text(text):
    """Escape plain text portions and apply inline formatting"""
    # Split by inline formatting markers to escape only the plain parts
    # We process inline formatting first to avoid double-escaping
    parts = re.split(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    result = []
    for part in parts:
        if re.match(r'\*\*\*.*?\*\*\*', part):
            inner = part[3:-3]
            result.append(r'\textbf{\textit{' + _escape_latex(inner) + '}}')
        elif re.match(r'\*\*.*?\*\*', part):
            inner = part[2:-2]
            result.append(r'\textbf{' + _escape_latex(inner) + '}')
        elif re.match(r'\*.*?\*', part):
            inner = part[1:-1]
            result.append(r'\textit{' + _escape_latex(inner) + '}')
        elif re.match(r'`.*?`', part):
            inner = part[1:-1]
            result.append(r'\texttt{' + _escape_latex(inner) + '}')
        else:
            result.append(_escape_latex(part))
    return ''.join(result)


def markdown_to_latex(content, params):
    """Convert Markdown content to a complete LaTeX document"""

    subject = _escape_latex(params.get("subject", ""))
    topic = _escape_latex(params.get("topic", ""))
    grade_level = _escape_latex(params.get("grade_level", ""))
    doc_type = _escape_latex(params.get("doc_type", "Document"))

    title = f"{subject} -- {doc_type}" if subject else doc_type

    preamble = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=2.5cm]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{amssymb}
\usepackage{hyperref}
\usepackage{lmodern}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue
}

"""

    doc_info = f"\\title{{\\textbf{{{title}}}}}\n"
    if topic:
        doc_info += f"\\date{{\\textit{{Topic: {topic}}}}}\n"
    else:
        doc_info += "\\date{}\n"
    doc_info += "\\author{}\n"

    body_lines = ["\\begin{document}", "\\maketitle", ""]
    if grade_level:
        body_lines.append(f"\\noindent\\textbf{{Grade Level:}} {grade_level}\\\\[6pt]")
        body_lines.append("")

    in_itemize = False
    in_enumerate = False

    lines = content.split('\n')

    def close_lists():
        nonlocal in_itemize, in_enumerate
        result = []
        if in_itemize:
            result.append("\\end{itemize}")
            in_itemize = False
        if in_enumerate:
            result.append("\\end{enumerate}")
            in_enumerate = False
        return result

    for line in lines:
        stripped = line.strip()

        if not stripped:
            body_lines.extend(close_lists())
            body_lines.append("")
            continue

        # Headings
        if stripped.startswith('#'):
            body_lines.extend(close_lists())
            hash_count = len(stripped) - len(stripped.lstrip('#'))
            heading_text = stripped[hash_count:].strip()
            heading_text = _process_text(heading_text)
            if hash_count == 1:
                body_lines.append(f"\\section{{{heading_text}}}")
            elif hash_count == 2:
                body_lines.append(f"\\subsection{{{heading_text}}}")
            elif hash_count == 3:
                body_lines.append(f"\\subsubsection{{{heading_text}}}")
            else:
                body_lines.append(f"\\paragraph{{{heading_text}}}")
            continue

        # Bullet list
        if re.match(r'^[-*•]\s', stripped):
            if in_enumerate:
                body_lines.extend(close_lists())
            if not in_itemize:
                body_lines.append("\\begin{itemize}[leftmargin=*]")
                in_itemize = True
            item_text = _process_text(stripped[2:].strip())
            body_lines.append(f"  \\item {item_text}")
            continue

        # Numbered list
        if re.match(r'^\d+[.)]\s', stripped):
            if in_itemize:
                body_lines.extend(close_lists())
            if not in_enumerate:
                body_lines.append("\\begin{enumerate}[leftmargin=*]")
                in_enumerate = True
            item_text = _process_text(re.sub(r'^\d+[.)]\s+', '', stripped))
            body_lines.append(f"  \\item {item_text}")
            continue

        # Horizontal rule
        if re.match(r'^[-*_]{3,}$', stripped):
            body_lines.extend(close_lists())
            body_lines.append("\\hrulefill")
            continue

        # Regular paragraph
        body_lines.extend(close_lists())
        body_lines.append(_process_text(stripped))

    body_lines.extend(close_lists())
    body_lines.append("")
    body_lines.append("\\end{document}")

    latex_source = preamble + doc_info + "\n" + "\n".join(body_lines)
    return latex_source.encode("utf-8")
