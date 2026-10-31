"""Sanitized JSON export of the current session's own execution only."""
import json
import re

SENSITIVE = re.compile(r'(?:api.?key|password|secret|authorization|credential|access.?token|refresh.?token|connection.?config|^(?:token|key|cookie|cookies)$)', re.I)
TOKENS = re.compile(r'AIza[\w-]{30,}|sk-(?:proj-)?[\w-]{20,}|hf_[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[^\s"\']+', re.I)
ASSIGNMENT = re.compile(r'(?i)((?:api[_-]?key|access[_-]?token|password|secret)\s*[=:]\s*)[^\s&"\'<>]+')


def execution_record_json(record, *, secrets=()):
    """Do not read shared server logs or include connection settings."""
    payload = record.model_dump(mode='json') if hasattr(record, 'model_dump') else dict(record)
    known = tuple(s for s in secrets if isinstance(s, str) and s)
    def clean(value):
        if isinstance(value, dict):
            return {k:('[REDACTED]' if SENSITIVE.search(k) else clean(v)) for k,v in value.items()}
        if isinstance(value, (list,tuple)):
            return [clean(v) for v in value]
        if isinstance(value, str):
            for secret in known:
                value = value.replace(secret, '[REDACTED]')
            value = TOKENS.sub('[REDACTED]', value)
            return ASSIGNMENT.sub(r'\1[REDACTED]', value)
        return value
    return (json.dumps(clean(payload), ensure_ascii=False, indent=2)+'\n').encode('utf-8')
