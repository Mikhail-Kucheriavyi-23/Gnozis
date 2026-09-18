"""Provenance obligations for accepted semantic transitions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .history import TransitionRecord


@dataclass(frozen=True)
class Provenance:
    candidate_hash: str
    evidence_hash: str
    kernel_version: str
    source_ids: tuple[str, ...] = ()

    def complete(self) -> bool:
        return bool(
            self.candidate_hash.strip()
            and self.evidence_hash.strip()
            and self.kernel_version.strip()
        )


def attach_provenance(
    record: TransitionRecord, provenance: Provenance
) -> TransitionRecord:
    if not provenance.complete():
        raise ValueError("incomplete provenance")
    if record.candidate_hash != provenance.candidate_hash:
        raise ValueError("candidate provenance mismatch")
    if record.evidence_hash != provenance.evidence_hash:
        raise ValueError("evidence provenance mismatch")
    if record.kernel_version != provenance.kernel_version:
        raise ValueError("kernel provenance mismatch")
    return record
