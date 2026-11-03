"""Project-local Google credentials precede unrelated global Windows keys."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_google_key():
    values = {}
    path = ROOT / '.env'
    if path.is_file():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            name, sep, value = line.strip().removeprefix('export ').partition('=')
            name = name.strip()
            if sep and name in ('GOOGLE_API_KEY', 'GEMINI_API_KEY') and name not in values:
                values[name] = value.strip().strip('"').strip("'")
    for name in ('GOOGLE_API_KEY', 'GEMINI_API_KEY'):
        if values.get(name):
            return values[name], '.env:' + name
    for name in ('GOOGLE_API_KEY', 'GEMINI_API_KEY'):
        if os.getenv(name):
            return os.getenv(name), 'environment:' + name
    return None, 'missing'
