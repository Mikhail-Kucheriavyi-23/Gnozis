"""Explicit conflict-resolution candidates.

Resolution proposes a candidate; it never performs semantic mutation.
The resulting Psi must pass Proof -> Admission -> SemanticCommit.
"""
from __future__ import annotations

from dataclasses import dataclass

from .merge import Conflict
from .state import Psi


@dataclass(frozen=True)
class ResolutionCandidate:
    conflict: Conflict
    candidate: Psi
    rationale: str

    @property
    def source_branches(self) -> tuple[Psi, Psi]:
        return self.conflict.left, self.conflict.right


def resolve(conflict: Conflict, candidate: Psi, rationale: str) -> ResolutionCandidate:
    """Wrap an explicitly supplied resolution as a candidate only."""
    if not isinstance(conflict, Conflict):
        raise TypeError("resolve requires a Conflict.")
    if not isinstance(candidate, Psi):
        raise TypeError("resolution candidate must be Psi.")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("resolution requires a non-empty rationale.")
    return ResolutionCandidate(
        conflict=conflict,
        candidate=candidate,
        rationale=rationale,
    )
