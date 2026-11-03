"""Shared generation pipeline used by every educational material module."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from experiment import ExecutionLogger, ExecutionRecord
from models import GenerationRequest
from processing import ProcessedResponse, process_response
from prompting import PromptArtifact
from providers import ProviderGateway, ProviderResponse


DocumentExporter = Callable[[str, GenerationRequest], bytes]


class RecordSink(Protocol):
    def append(self, record: ExecutionRecord) -> None: ...


@dataclass(frozen=True, slots=True)
class GenerationOutcome:
    """Internal result with a compatibility view for the current Streamlit UI."""

    success: bool
    execution_id: str
    content: str | None = None
    docx_file: bytes | None = None
    request: GenerationRequest | None = None
    prompt_artifact: PromptArtifact | None = None
    provider_response: ProviderResponse | None = None
    processed_response: ProcessedResponse | None = None
    execution_record: ExecutionRecord | None = None
    error: str | None = None

    def as_legacy_dict(self) -> dict[str, Any]:
        """Keep the existing UI contract while presentation is migrated later."""

        result = {
            "success": self.success,
            "execution_id": self.execution_id,
        }
        if self.success:
            result.update(
                content=self.content,
                docx_file=self.docx_file,
                request=self.request,
                prompt_artifact=self.prompt_artifact,
                provider_response=self.provider_response,
                processed_response=self.processed_response,
                execution_record=self.execution_record,
            )
        else:
            result["error"] = self.error
        return result


def _prompt_record(prompt: PromptArtifact) -> dict[str, Any]:
    return {
        "text": prompt.text,
        "template_version": prompt.template_version,
        "sha256": prompt.sha256,
        "semantic_payload_hash": prompt.semantic_payload_hash,
        "expected_requirements": list(prompt.expected_requirements),
    }


def execute_generation(
    request: GenerationRequest,
    prompt: PromptArtifact,
    connection_config: Mapping[str, Any],
    exporter: DocumentExporter,
    *,
    gateway: ProviderGateway | None = None,
    record_sink: RecordSink | None = None,
) -> GenerationOutcome:
    """Run the provider-neutral generation, export and audit pipeline once."""

    selected_gateway = gateway or ProviderGateway()
    selected_sink = record_sink or ExecutionLogger()
    provider_response: ProviderResponse | None = None
    processed_response: ProcessedResponse | None = None

    try:
        provider_response = selected_gateway.generate(request, prompt, connection_config)
        processed_response = process_response(provider_response.content)
        docx_file = exporter(processed_response.content, request)
        record = ExecutionRecord(
            execution_id=str(request.execution_id),
            status="success",
            request=request.model_dump(mode="json"),
            prompt=_prompt_record(prompt),
            provider_response=provider_response.model_dump(mode="json", exclude={"content"}),
            raw_response=processed_response.raw_content,
            processed_response=processed_response.content,
            processing_warnings=processed_response.warnings,
        )
        selected_sink.append(record)
        return GenerationOutcome(
            success=True,
            execution_id=str(request.execution_id),
            content=processed_response.content,
            docx_file=docx_file,
            request=request,
            prompt_artifact=prompt,
            provider_response=provider_response,
            processed_response=processed_response,
            execution_record=record,
        )
    except Exception as error:
        record = ExecutionRecord(
            execution_id=str(request.execution_id),
            status="error",
            request=request.model_dump(mode="json"),
            prompt=_prompt_record(prompt),
            provider_response=(
                provider_response.model_dump(mode="json", exclude={"content"})
                if provider_response
                else {}
            ),
            raw_response=processed_response.raw_content if processed_response else "",
            processed_response=processed_response.content if processed_response else "",
            processing_warnings=processed_response.warnings if processed_response else [],
            error=str(error),
        )
        try:
            selected_sink.append(record)
        except Exception:
            # The generation error is primary and must not be hidden by a logging failure.
            pass
        return GenerationOutcome(
            success=False,
            execution_id=str(request.execution_id),
            request=request,
            prompt_artifact=prompt,
            provider_response=provider_response,
            processed_response=processed_response,
            execution_record=record,
            error=str(error),
        )
