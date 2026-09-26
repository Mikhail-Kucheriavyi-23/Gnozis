"""Explicit opt-in execution request derived from admitted information."""
from __future__ import annotations

from dataclasses import dataclass

from .external_operation import ExternalOperation
from .information_contract import Information


@dataclass(frozen=True)
class ExternalExecutionRequest:
    information_id: str
    operation: ExternalOperation
    content_digest: str
    purpose: str

    @classmethod
    def from_information(
        cls,
        information: Information,
        *,
        operation: ExternalOperation,
        content_digest: str,
        purpose: str,
    ) -> "ExternalExecutionRequest":
        information.require_authorized()
        if not purpose.strip():
            raise ValueError("execution purpose is required")
        if not content_digest.strip():
            raise ValueError("content_digest is required")
        return cls(
            information_id=information.information_id,
            operation=operation,
            content_digest=content_digest,
            purpose=purpose,
        )
