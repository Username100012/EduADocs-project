"""Tests for the frozen and reproducible LLM-judge execution manifest."""

from datetime import datetime, timezone
import json
import sys
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    JudgeAttemptPolicy,
    JudgeConfiguration,
    JudgeExecutionManifest,
    JudgeResponseErrorCode,
    REQUIRED_ARTIFACTS,
    fingerprint_artifact,
    fingerprint_required_judge_artifacts,
)


def configuration() -> JudgeConfiguration:
    return JudgeConfiguration(
        provider="approved-provider",
        model="immutable-model-id",
        model_version="immutable-version-id",
        temperature=0,
        seed=42,
        max_output_tokens=1200,
        provider_parameters={"top_p": 1},
    )


def manifest() -> JudgeExecutionManifest:
    return JudgeExecutionManifest(
        manifest_id="judge-manifest-test-v1",
        frozen_at=datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc),
        judge_configuration=configuration(),
        artifacts=fingerprint_required_judge_artifacts(ROOT_DIR),
    )


class LlmJudgeManifestTests(unittest.TestCase):
    def test_checked_in_manifest_is_valid_and_artifacts_are_unchanged(self):
        manifest_path = ROOT_DIR / "experiments" / "judge_execution_manifest.v1.json"
        frozen = JudgeExecutionManifest.model_validate_json(
            manifest_path.read_text(encoding="utf-8"), strict=True
        )
        recorded = {
            artifact.artifact_id: artifact.sha256 for artifact in frozen.artifacts
        }
        current = {
            artifact.artifact_id: artifact.sha256
            for artifact in fingerprint_required_judge_artifacts(ROOT_DIR)
        }
        expected_hash = (
            ROOT_DIR
            / "experiments"
            / "judge_execution_manifest.v1.canonical.sha256"
        ).read_text(encoding="utf-8").split()[0]

        self.assertEqual(recorded, current)
        self.assertEqual(frozen.manifest_hash, expected_hash)

    def test_freezes_configuration_repetitions_attempts_and_blinding(self):
        value = manifest()
        self.assertEqual(value.status, "frozen")
        self.assertEqual(value.repetitions_per_response, 3)
        self.assertEqual(value.attempt_policy.max_attempts_per_repetition, 2)
        self.assertTrue(value.attempt_policy.preserve_every_attempt)
        self.assertFalse(value.attempt_policy.replace_failed_repetition)
        self.assertTrue(value.blinding_policy.hide_condition)
        self.assertEqual(
            set(value.attempt_policy.retry_validation_errors_once),
            set(JudgeResponseErrorCode),
        )

    def test_contains_exact_required_artifacts_with_real_hashes(self):
        value = manifest()
        self.assertEqual(
            {artifact.artifact_id for artifact in value.artifacts},
            set(REQUIRED_ARTIFACTS),
        )
        self.assertTrue(all(len(artifact.sha256) == 64 for artifact in value.artifacts))

    def test_manifest_hash_is_deterministic_and_changes_with_configuration(self):
        first = manifest()
        second = manifest()
        self.assertEqual(first.manifest_hash, second.manifest_hash)

        changed = first.model_copy(
            update={"judge_configuration": configuration().model_copy(update={"seed": 7})}
        )
        self.assertNotEqual(first.manifest_hash, changed.manifest_hash)

    def test_save_is_create_only_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "judge_manifest.json"
            value = manifest()
            value.save_frozen(path)
            original = path.read_bytes()

            with self.assertRaises(FileExistsError):
                value.save_frozen(path)

            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(json.loads(original)["repetitions_per_response"], 3)

    def test_rejects_incomplete_artifact_set_and_retry_policy(self):
        with self.assertRaises(ValidationError):
            JudgeExecutionManifest(
                manifest_id="judge-manifest-invalid",
                frozen_at=datetime.now(timezone.utc),
                judge_configuration=configuration(),
                artifacts=fingerprint_required_judge_artifacts(ROOT_DIR)[:-1],
            )

        with self.assertRaises(ValidationError):
            JudgeAttemptPolicy(
                retry_validation_errors_once=(JudgeResponseErrorCode.INVALID_JSON,)
            )

    def test_rejects_artifacts_outside_workspace(self):
        with self.assertRaises(ValueError):
            fingerprint_artifact(ROOT_DIR, "unsafe", "../outside.txt")


if __name__ == "__main__":
    unittest.main()
