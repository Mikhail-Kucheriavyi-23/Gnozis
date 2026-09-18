"""Explicit conflict-resolution candidates."""
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
    def source_branches(self):
        return self.conflict.left, self.conflict.right

    @property
    def source_psis(self):
        return self.conflict.source_psis


def resolve(conflict: Conflict, candidate: Psi, rationale: str) -> ResolutionCandidate:
    if not isinstance(conflict, Conflict):
        raise TypeError("resolve requires a Conflict.")
    if not isinstance(candidate, Psi):
        raise TypeError("resolution candidate must be Psi.")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("resolution requires a non-empty rationale.")
    return ResolutionCandidate(conflict=conflict, candidate=candidate, rationale=rationale)
