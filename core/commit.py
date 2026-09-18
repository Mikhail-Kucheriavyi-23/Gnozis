"""Canonical semantic commit boundary."""
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

    def apply(
        self,
        history: AppendOnlyHistory | None = None,
        record: TransitionRecord | None = None,
    ) -> Psi:
        candidate = require_admitted(self.admission)
        canonical = canonicalize_psi(candidate)
        if history is None or record is None:
            return canonical.psi

        result: CommitResult[Psi] = commit_once(
            history,
            record,
            self.previous,
            canonical.psi,
        )
        return result.value


def commit(previous: Psi, admission: Admission) -> SemanticCommit:
    if not isinstance(previous, Psi):
        raise TypeError("previous must be Psi.")
    return SemanticCommit(previous=previous, admission=admission)
