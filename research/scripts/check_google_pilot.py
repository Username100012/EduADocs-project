"""Check SDK locally; --live explicitly enables one preflight API call."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from models import GenerationRequest, LessonPlanParameters
from prompting import PromptArtifact
from providers.google_adapter import GoogleAdapter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT / "experiments/pilot_config.json").read_text())
    generator = config["generators"]["gemini"]
    from google.genai import types
    types.GenerateContentConfig(**generator["generation_config"])
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "sdk_version": version("google-genai"), "model": generator["model"],
        "configuration_valid": True, "live_requested": args.live,
        "api_called": False, "status": "local_configuration_valid",
        "experimental_data": False,
    }
    if args.live:
        from google_credentials import read_google_key
        key, source = read_google_key()
        report["credential_source"] = source
        if not key:
            report["status"] = "credential_missing"
        else:
            request = GenerationRequest(
                subject="Compatibilidade", topic="Teste técnico", grade_level="Superior",
                document_type="lesson_plan", provider="google", model=generator["model"],
                max_tokens=generator["generation_config"]["max_output_tokens"],
                pedagogical_parameters=LessonPlanParameters(),
            )
            report["api_called"] = True
            try:
                response = GoogleAdapter().generate(
                    request, PromptArtifact("Responda somente: COMPATIBILIDADE_OK", "preflight-v1", ()),
                    {"api_key": key, "single_attempt": True, "timeout_ms": 60000},
                )
                report["response"] = response.model_dump(mode="json")
                report["status"] = (
                    "compatible" if response.content.strip() == "COMPATIBILIDADE_OK"
                    and response.finish_reason == "STOP" else "unexpected_response"
                )
            except Exception as error:
                # Provider messages can contain request data; retain only safe classification.
                report["status"] = "api_error"
                report["error_type"] = type(error).__name__
                code = getattr(error, "code", None)
                report["error_code"] = code if isinstance(code, (int, str)) else None
    output = ROOT / "artifacts/google_pilot_compatibility.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "sdk_version", "api_called")}, indent=2))
    return 0 if report["status"] in {"compatible", "local_configuration_valid"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
