"""One technical judge preflight, outside collection; never print credentials."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys
from time import perf_counter

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.judge_response import parse_llm_judge_response, JudgeResponseValidationError


def wire_schema(value):
    """Equivalent string const -> enum for the API subset; preserve local schema."""
    if isinstance(value, list):
        return [wire_schema(v) for v in value]
    if not isinstance(value, dict):
        return value
    result = {k: wire_schema(v) for k, v in value.items() if k not in {"$schema", "$id", "const"}}
    if "const" in value:
        result.update(type="string", enum=[value["const"]])
    return result


def request_body(config, prompt, schema):
    p = config["provider_parameters"]
    body = {"model": config["model"], "input": prompt,
            "max_output_tokens": config["max_output_tokens"],
            "reasoning": {"effort": p["reasoning_effort"]}, "store": p["store"],
            # Protocol's 'standard' tier corresponds to wire API 'default'.
            "service_tier": "default" if p["service_tier"] == "standard" else p["service_tier"],
            "text": {"format": {"type": "json_schema", "name": "eduadocs_judge",
                                "strict": p["strict_schema"], "schema": wire_schema(schema)}}}
    if config.get("temperature") is not None:
        body["temperature"] = config["temperature"]
    if p.get("top_p") is not None:
        body["top_p"] = p["top_p"]
    return body


def read_key():
    """Prefer this project's explicit credential over a global Windows key."""
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            name, sep, value = line.strip().removeprefix("export ").partition("=")
            if sep and name.strip() == "OPENAI_API_KEY":
                value = value.strip().strip('"').strip("'")
                if value:
                    return value
    return os.getenv("OPENAI_API_KEY") or None


def redact(value, key):
    serialized = json.dumps(value, ensure_ascii=False).replace(key, "[REDACTED]")
    return json.loads(re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED]", serialized))


def main(live):
    key = read_key()
    if not key:
        raise SystemExit("OPENAI_API_KEY ausente; nenhuma chamada realizada.")
    config = json.loads((ROOT / "experiments/judge_model_selection.v1.json").read_text(encoding="utf-8"))["judge_configuration"]
    row = json.loads((ROOT / "artifacts/pilot-qwen3-local/judge_queue.jsonl").read_text(encoding="utf-8").splitlines()[0])
    evaluation_id = "eval-" + sha256((row["evaluation_id"] + "technical-preflight").encode()).hexdigest()[:32]
    prompt = row["prompt"].replace(row["evaluation_id"], evaluation_id)
    schema = json.loads((ROOT / "experiments/llm_judge_response.schema.json").read_text(encoding="utf-8"))
    body = request_body(config, prompt, schema)
    report = {"experimental_data": False, "purpose": "single technical preflight, not pilot judgment",
              "credential_present": True, "model": config["model"],
              "evaluation_id": evaluation_id, "api_request": body,
              "local_schema_sha256": sha256(json.dumps(schema, sort_keys=True).encode()).hexdigest(),
              "status": "not_called", "automatic_retries": 0}
    if live:
        headers = {"Authorization": "Bearer " + key}
        try:
            model = requests.get("https://api.openai.com/v1/models/" + config["model"], headers=headers, timeout=30)
            report["model_access"] = {"http_status": model.status_code, "body": model.json()}
            if not model.ok:
                report["status"] = "model_access_failed"
            else:
                start = perf_counter()
                response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=body, timeout=90)
                report.update(latency_ms=(perf_counter() - start) * 1000, http_status=response.status_code,
                              request_id=response.headers.get("x-request-id"), raw_response=response.json())
                if not response.ok:
                    report["status"] = "generation_failed"
                else:
                    raw = report["raw_response"]
                    text = "".join(c["text"] for item in raw.get("output", [])
                                   for c in item.get("content", []) if c.get("type") == "output_text")
                    report["usage"] = raw.get("usage")
                    if raw.get("status") != "completed":
                        report["status"] = "incomplete_response"
                    else:
                        try:
                            parsed = parse_llm_judge_response(text, evaluation_id)
                            report.update(status="validated", validated_response=parsed.model_dump(mode="json"))
                        except JudgeResponseValidationError as error:
                            report.update(status="validation_failed", validation_error=str(error.code))
        except (requests.RequestException, ValueError) as error:
            report.update(status="transport_or_decode_failed", error_type=type(error).__name__)
    directory = ROOT / "artifacts/openai-judge-preflight" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory.mkdir(parents=True)
    report = redact(report, key)
    (directory / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in {"api_request", "raw_response", "validated_response"}}, ensure_ascii=True, indent=2))
    print("Report: " + str(directory.relative_to(ROOT) / "report.json"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    main(parser.parse_args().live)
