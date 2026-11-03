"""Local protocol freeze: one configuration, one checksum, no API calls."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = (
    'docs/MAIN_STUDY_PROTOCOL.md',
    'experiments/task_catalog.schema.json',
    'experiments/judge_response.v2.schema.json',
    'requirements.txt',
    'src/experiment/main_protocol.py',
    'src/experiment/pilot_runner.py',
    'src/experiment/prompt_conditions.py',
    'src/experiment/semantic_payload.py',
    'src/experiment/task_catalog.py',
    'src/experiment/task_prompt_set.py',
    'src/experiment/requirement_measurement.py',
    'src/experiment/automatic_metrics.py',
    'src/experiment/automatic_metrics_v2.py',
    'src/experiment/judge_response.py',
    'src/experiment/judge_contract_v2.py',
    'src/models/generation_request.py',
    'src/models/__init__.py',
    'src/prompting/models.py',
    'src/prompting/__init__.py',
    'src/providers/google_adapter.py',
    'src/providers/ollama_adapter.py',
    'src/providers/models.py',
    'src/providers/base.py',
    'src/providers/common.py',
    'scripts/prepare_main_study.py',
    'scripts/run_pilot.py',
    'scripts/google_credentials.py',
    'scripts/prepare_requirement_judgments.py',
    'scripts/run_requirement_judgments.py',
    'scripts/report_requirement_results.py',
    'scripts/check_openai_judge.py',
    'scripts/evaluate_pilot.py',
    'scripts/observe_saved_requirements.py',
)


def canonical_hash(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def verify_frozen(config_path, *, root=ROOT):
    """Refuse config, source, task or prompt drift before starting paid calls."""
    path = Path(config_path)
    config = json.loads(path.read_text(encoding='utf-8'))
    if config.get('protocol_version') != 'eduadocs-main-v1.0.0' or config.get('status') != 'ready_for_collection':
        raise ValueError('main protocol is not frozen for collection')
    seal = path.with_suffix(path.suffix + '.sha256')
    parts = seal.read_text(encoding='utf-8').split() if seal.is_file() else []
    if not parts or parts[0] != sha256(path.read_bytes()).hexdigest():
        raise ValueError('frozen configuration checksum mismatch')
    frozen = config.get('freeze', {})
    artifacts = frozen.get('artifact_sha256', {})
    if set(artifacts) != set(ARTIFACTS):
        raise ValueError('frozen artifact list mismatch')
    for name, expected in artifacts.items():
        artifact = Path(root)/name
        if not artifact.is_file() or sha256(artifact.read_bytes()).hexdigest() != expected:
            raise ValueError('frozen artifact changed: '+name)
    from experiment.pilot_runner import build_plan
    if canonical_hash(config['tasks']) != frozen.get('catalog_sha256'):
        raise ValueError('frozen catalog mismatch')
    if canonical_hash(build_plan(config)) != frozen.get('prompt_plan_sha256'):
        raise ValueError('frozen prompt plan mismatch')
    return config
