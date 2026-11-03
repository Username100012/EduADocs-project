"""Report credential precedence without printing secrets or making API calls."""
import json
import os
from pathlib import Path


def diagnose():
    rows = []
    for line in (Path(__file__).resolve().parents[1] / '.env').read_text(encoding='utf-8-sig').splitlines():
        name, sep, value = line.strip().removeprefix('export ').partition('=')
        if sep and name.strip() == 'OPENAI_API_KEY':
            rows.append(value.strip().strip('"').strip("'"))
    environment = os.getenv('OPENAI_API_KEY')
    dotenv = rows[0] if rows else None  # Matches check_openai_judge.read_key.
    report = {'environment_present': bool(environment), 'dotenv_entries': len(rows),
              'dotenv_present': bool(dotenv),
              'same_credential': environment == dotenv if environment and dotenv else None,
              'effective_source': 'dotenv_first_entry' if dotenv else 'environment',
              'dotenv_contains_whitespace': any(c.isspace() for c in dotenv) if dotenv else None,
              'dotenv_has_project_key_prefix': dotenv.startswith('sk-proj-') if dotenv else None}
    if os.name == 'nt':
        import winreg
        for label, hive, path in (
                ('user', winreg.HKEY_CURRENT_USER, 'Environment'),
                ('machine', winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')):
            try:
                with winreg.OpenKey(hive, path) as key:
                    value, _ = winreg.QueryValueEx(key, 'OPENAI_API_KEY')
                report[label + '_persistent_present'] = bool(value)
                report[label + '_persistent_matches_dotenv'] = value == dotenv if dotenv else None
            except FileNotFoundError:
                report[label + '_persistent_present'] = False
    return report


if __name__ == '__main__':
    import sys
    report = diagnose()
    if '--check-access' in sys.argv:
        import requests
        from check_openai_judge import read_key
        key = read_key()
        if key:
            try:
                response = requests.get('https://api.openai.com/v1/models',
                    headers={'Authorization': 'Bearer ' + key}, timeout=30)
                report['access_http_status'] = response.status_code
                report['access_accepted'] = response.ok
            except requests.RequestException as error:
                report['access_error'] = type(error).__name__
        else:
            report['access_error'] = 'credential_absent'
    print(json.dumps(report))
