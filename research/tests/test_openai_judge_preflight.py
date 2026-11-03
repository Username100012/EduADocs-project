"""Preflight request preserves protocol and redacts credentials offline."""

import importlib.util
import json
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_openai_judge", ROOT / "scripts/check_openai_judge.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class JudgePreflightTests(unittest.TestCase):
    def test_wire_parameters_and_const_conversion_preserve_configuration(self):
        config = json.loads((ROOT / "experiments/judge_model_selection.v1.json").read_text(encoding="utf-8"))["judge_configuration"]
        before = json.dumps(config, sort_keys=True)
        schema = {"properties": {"version": {"const": "v1"}}}
        request = module.request_body(config, "test", schema)
        self.assertEqual(request["service_tier"], "default")
        self.assertFalse(request["store"])
        self.assertEqual(request["model"], config["model"])
        self.assertEqual(request["text"]["format"]["schema"]["properties"]["version"], {"type": "string", "enum": ["v1"]})
        self.assertEqual(schema, {"properties": {"version": {"const": "v1"}}})
        self.assertEqual(json.dumps(config, sort_keys=True), before)

    def test_nested_error_credentials_are_removed(self):
        key = "synthetic-secret"
        result = module.redact({"error": {"message": "credential " + key + " sk-fake123"}}, key)
        self.assertNotIn(key, json.dumps(result))
        self.assertNotIn("sk-fake123", json.dumps(result))

    def test_project_key_precedes_global_key_without_mutating_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(module, 'ROOT', root), patch.dict(module.os.environ, {'OPENAI_API_KEY': 'global-test-key'}):
                self.assertEqual(module.read_key(), 'global-test-key')
                (root / '.env').write_text('OPENAI_API_KEY="project-test-key"\n', encoding='utf-8')
                self.assertEqual(module.read_key(), 'project-test-key')
                self.assertEqual(module.os.getenv('OPENAI_API_KEY'), 'global-test-key')
                (root / '.env').write_text('OPENAI_API_KEY=\n', encoding='utf-8')
                self.assertEqual(module.read_key(), 'global-test-key')
