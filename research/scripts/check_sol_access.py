"""Single technical Sol request, outside either sensitivity collection."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

import requests

from check_openai_judge import read_key, redact
from run_judge_sensitivity import build_plan
from experiment.judge_response import parse_llm_judge_response, JudgeResponseValidationError

ROOT = Path(__file__).resolve().parents[1]


def main():
    key = read_key()
    if not key:
        raise SystemExit("OpenAI credential absent")
    plan = build_plan("gpt-6.1-sol")
    job = next(j for j in plan["jobs"] if j["kind"] == "baseline")
    eid = "eval-" + sha256((job["evaluation_id"] + ":sol-technical-preflight").encode()).hexdigest()[:32]
    body = dict(job["body"])
    body["input"] = body["input"].replace(job["evaluation_id"], eid)
    report = {"experimental_data": False, "model": plan["configuration"]["model"],
              "api_request": body, "evaluation_id": eid, "status": "not_called", "automatic_retries": 0}
    try:
        headers = {"Authorization": "Bearer " + key}
        response = requests.get("https://api.openai.com/v1/models/gpt-6.1-sol", headers=headers, timeout=30)
        report["model_access"] = {"http_status": response.status_code, "body": redact(response.json(), key)}
        if response.ok:
            start = perf_counter()
            response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=body, timeout=90)
            raw = redact(response.json(), key)
            report.update(http_status=response.status_code, raw_response=raw,
                          latency_ms=(perf_counter() - start) * 1000, request_id=response.headers.get("x-request-id"))
            report["status"] = "api_error"
            if response.ok and raw.get("status") == "completed" and raw.get("model") == "gpt-6.1-sol":
                text = "".join(c["text"] for item in raw.get("output", []) for c in item.get("content", []) if c.get("type") == "output_text")
                try:
                    parsed = parse_llm_judge_response(text, eid)
                    report.update(status="validated", validated_response=parsed.model_dump(mode="json"), usage=raw.get("usage"))
                except JudgeResponseValidationError as error:
                    report.update(status="validation_error", error=error.code.value)
            elif response.ok:
                report["status"] = "incomplete_or_different_model"
        else:
            report["status"] = "model_access_failed"
    except (requests.RequestException, ValueError) as error:
        report.update(status="transport_error", error=type(error).__name__)
    directory = ROOT / "artifacts/sol-preflight" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory.mkdir(parents=True)
    (directory / "report.json").write_text(json.dumps(redact(report, key), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in {"api_request", "raw_response", "validated_response"}}, ensure_ascii=True, indent=2))
    print(str(directory.relative_to(ROOT) / "report.json"))


if __name__ == "__main__":
    main()
