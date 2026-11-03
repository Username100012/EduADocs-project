"""Tests for the twelve-task experimental catalog schema."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from experiment import (  # noqa: E402
    ExperimentalTaskCatalog,
    ExperimentalTaskDefinition,
    LessonPlanSemanticPayload,
)


def task(number: int) -> ExperimentalTaskDefinition:
    return ExperimentalTaskDefinition(
        task_id=f"task-{number:03d}",
        subject_area=f"Área {number}",
        payload=LessonPlanSemanticPayload(
            topic=f"Tópico {number}",
            grade_level=f"Nível {number}",
            learning_objectives=f"Objetivo {number}",
            duration_minutes=40 + number,
            methodology=f"Metodologia {number}",
            materials=f"Materiais {number}",
            assessment_strategy=f"Avaliação {number}",
        ),
    )


def catalog() -> ExperimentalTaskCatalog:
    return ExperimentalTaskCatalog(
        catalog_id="catalog-test-v1",
        tasks=[task(number) for number in range(1, 13)],
    )


class TaskCatalogTests(unittest.TestCase):
    def test_requires_exactly_twelve_tasks(self):
        with self.assertRaises(ValidationError):
            ExperimentalTaskCatalog(catalog_id="too-small", tasks=[task(1)])
        self.assertEqual(len(catalog().tasks), 12)

    def test_rejects_duplicate_ids(self):
        tasks = [task(number) for number in range(1, 13)]
        tasks[-1] = tasks[0].model_copy()
        with self.assertRaisesRegex(ValidationError, "task_id values must be unique"):
            ExperimentalTaskCatalog(catalog_id="duplicates", tasks=tasks)

    def test_rejects_duplicate_semantic_payloads(self):
        tasks = [task(number) for number in range(1, 13)]
        tasks[-1] = tasks[-1].model_copy(update={"payload": tasks[0].payload})
        with self.assertRaisesRegex(ValidationError, "unique semantic payloads"):
            ExperimentalTaskCatalog(catalog_id="duplicates", tasks=tasks)

    def test_builds_twelve_valid_prompt_sets(self):
        prompt_sets = catalog().build_prompt_sets()
        self.assertEqual(len(prompt_sets), 12)
        self.assertEqual(prompt_sets[0].task_id, "task-001")
        self.assertEqual(tuple(prompt_sets[0].conditions), ("c0", "c1", "c2"))

    def test_save_load_and_hash_are_deterministic(self):
        original = catalog()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            original.save(path)
            loaded = ExperimentalTaskCatalog.load(path)

        self.assertEqual(original, loaded)
        self.assertEqual(original.canonical_json(), loaded.canonical_json())
        self.assertEqual(original.catalog_hash, loaded.catalog_hash)

    def test_checked_in_json_schema_is_valid_json(self):
        schema_path = SRC_DIR.parent / "experiments" / "task_catalog.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["tasks"]["minItems"], 12)
        self.assertEqual(schema["properties"]["tasks"]["maxItems"], 12)


if __name__ == "__main__":
    unittest.main()
