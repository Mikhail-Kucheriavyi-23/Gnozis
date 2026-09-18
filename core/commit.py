"""Canonical semantic commit boundary with mandatory causal history."""
from __future__ import annotations

from dataclasses import dataclass

from .admission import Admission, require_admitted
from .canonical_boundary import canonicalize_psi
from .commit_contract import CommitResult, commit_once
from .history import AppendOnlyHistory, TransitionRecord
from .state import Psi


@dataclass(frozen=True)
class SemanticCommit:
    previous: Psi
    admission: Admission
    kernel_version: str

    def apply(self, history: AppendOnlyHistory) -> tuple[Psi, AppendOnlyHistory]:
        candidate = require_admitted(self.admission)
        canonical = canonicalize_psi(candidate)
        head = history.head
        sequence = 0 if head is None else head.sequence + 1
        previous_hash = "genesis" if head is None else head.state_hash
        record = TransitionRecord(
            sequence=sequence,
            previous_hash=previous_hash,
            state_hash=_state_hash(canonical.psi),
            kernel_version=self.kernel_version,
            candidate_hash=_state_hash(canonical.psi),
            admitted=True,
        )
        result: CommitResult[Psi] = commit_once(
            history,
            record,
            self.previous,
            canonical.psi,
        )
        return result.value, result.history


def _state_hash(psi: Psi) -> str:
    return str(hash(repr((psi.x, psi.relations))))


def commit(previous: Psi, admission: Admission, kernel_version: str) -> SemanticCommit:
    if not isinstance(previous, Psi):
        raise TypeError("previous must be Psi.")
    if not kernel_version.strip():
        raise ValueError("kernel_version is required.")
    return SemanticCommit(
        previous=previous,
        admission=admission,
        kernel_version=kernel_version,
    )
