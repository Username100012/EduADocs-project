"""Schema and file I/O for the twelve-task experimental catalog."""

from hashlib import sha256
import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from experiment.semantic_payload import LessonPlanSemanticPayload
from experiment.task_prompt_set import (
    ExperimentalTaskPromptSet,
    build_experimental_task_prompt_set,
)


NonEmptyText = Annotated[str, Field(min_length=1)]


class CatalogModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=True)


class ExperimentalTaskDefinition(CatalogModel):
    """One catalog entry: metadata plus the seven controlled requirements."""

    task_id: str = Field(pattern=r"^task-\d{3}$")
    subject_area: NonEmptyText
    payload: LessonPlanSemanticPayload

    def build_prompt_set(self) -> ExperimentalTaskPromptSet:
        return build_experimental_task_prompt_set(self.task_id, self.payload)


class ExperimentalTaskCatalog(CatalogModel):
    """Versioned catalog containing exactly twelve unique lesson-plan tasks."""

    schema_version: Literal["eduadocs-task-catalog-v1.0.0"] = (
        "eduadocs-task-catalog-v1.0.0"
    )
    catalog_id: NonEmptyText
    language: Literal["pt-BR"] = "pt-BR"
    tasks: list[ExperimentalTaskDefinition] = Field(min_length=12, max_length=12)

    @model_validator(mode="after")
    def validate_unique_tasks(self) -> "ExperimentalTaskCatalog":
        task_ids = [task.task_id for task in self.tasks]
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("task_id values must be unique")

        semantic_hashes = [task.payload.semantic_hash for task in self.tasks]
        if len(semantic_hashes) != len(set(semantic_hashes)):
            raise ValueError("experimental tasks must have unique semantic payloads")
        return self

    def canonical_json(self) -> str:
        """Stable UTF-8 representation used for catalog identification."""

        return json.dumps(
            self.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    @property
    def catalog_hash(self) -> str:
        return sha256(self.canonical_json().encode("utf-8")).hexdigest()

    def build_prompt_sets(self) -> tuple[ExperimentalTaskPromptSet, ...]:
        """Build all prompt bundles without invoking any provider."""

        return tuple(task.build_prompt_set() for task in self.tasks)

    @classmethod
    def load(cls, path: Path | str) -> "ExperimentalTaskCatalog":
        """Read and validate one UTF-8 JSON catalog file."""

        catalog_path = Path(path)
        with catalog_path.open("r", encoding="utf-8") as stream:
            return cls.model_validate(json.load(stream))

    def save(self, path: Path | str) -> None:
        """Write a human-readable deterministic JSON catalog."""

        catalog_path = Path(path)
        catalog_path.parent.mkdir(parents=True, exist_ok=True)
        catalog_path.write_text(
            json.dumps(
                self.model_dump(mode="json"),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
