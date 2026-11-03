"""Read model availability and capture one sanitized Gemini diagnostic error."""

import argparse
import json
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    from google import genai
    from google.genai import types
    from google_credentials import read_google_key
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT/'experiments/pilot_config.json')
    parser.add_argument('--output', type=Path, default=ROOT/'artifacts/google_access_diagnostic.json')
    parser.add_argument('--skip-list', action='store_true')
    args = parser.parse_args()
    key, source = read_google_key()
    if not key:
        raise SystemExit("No local credential found")

    def clean(value):
        if isinstance(value, dict):
            return {k: "[REDACTED]" if re.search(r"key|authorization|credential|secret", k, re.I)
                    else clean(v) for k, v in value.items()}
        if isinstance(value, list):
            return [clean(v) for v in value]
        if isinstance(value, str):
            value = value.replace(key, "[REDACTED]")
            return re.sub(r"AIza[\w-]+", "[REDACTED]", value)
        if value is None or isinstance(value, (int, float, bool)):
            return value
        return clean(str(value))

    def error_details(error):
        return clean({"type": type(error).__name__, "code": getattr(error, "code", None),
                      "message": getattr(error, "message", str(error)),
                      "details": getattr(error, "details", None)})

    config = json.loads(args.config.read_text(encoding="utf-8"))
    model = config["generators"]["gemini"]["model"]
    report = {"at": datetime.now(timezone.utc).isoformat(), "credential_source": source,
              "configured_model": model, "experimental_data": False,
              "configuration_path": str(args.config),
              "billing_and_project_limits": "Not accessible from model inference credentials alone; inspect AI Studio usage and billing."}
    options = types.HttpOptions(timeout=60000, retry_options=types.HttpRetryOptions(attempts=1))
    with genai.Client(api_key=key, http_options=options) as client:
        try:
            models = []
            for entry in ([] if args.skip_list else client.models.list(config={"page_size": 100})):
                models.append({"name": entry.name,
                               "supported_actions": getattr(entry, "supported_actions", None)})
            report["models"] = clean(models)
            report["model_list_skipped"] = args.skip_list
            report["configured_model_listed"] = None if args.skip_list else any(
                m["name"].removeprefix("models/") == model for m in models)
        except Exception as error:
            report["model_list_error"] = error_details(error)
        try:
            entry = client.models.get(model=model)
            report["model_get"] = clean(entry.model_dump(mode="json", exclude_none=True))
        except Exception as error:
            report["model_get_error"] = error_details(error)
        try:
            result = client.models.generate_content(
                model=model, contents="Responda somente: OK",
                config=types.GenerateContentConfig(
                    **config["generators"]["gemini"]["generation_config"]),
            )
            report["generation"] = clean({"text": result.text,
                                         "model_version": result.model_version,
                                         "usage": result.usage_metadata.model_dump(mode="json") if result.usage_metadata else None})
        except Exception as error:
            report["generation_error"] = error_details(error)
    report = clean(report)
    path = args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in {"models", "model_get"}},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
