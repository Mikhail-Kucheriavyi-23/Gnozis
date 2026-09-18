"""Canonical semantic commit boundary.

PsiTransition computes a candidate Psi. It does not itself mutate semantic
state. Only an admitted candidate can cross this commit boundary.
"""
from __future__ import annotations

from dataclasses import dataclass

from .admission import Admission, require_admitted
from .state import Psi


@dataclass(frozen=True)
class SemanticCommit:
    """Accepted semantic transition from one Psi to another."""

    previous: Psi
    admission: Admission

    def apply(self) -> Psi:
        candidate = require_admitted(self.admission)
        if not isinstance(candidate, Psi):
            raise TypeError("SemanticCommit requires an admitted Psi candidate.")
        return candidate


def commit(previous: Psi, admission: Admission) -> SemanticCommit:
    """Construct the only canonical semantic commit object."""
    if not isinstance(previous, Psi):
        raise TypeError("previous must be Psi.")
    return SemanticCommit(previous=previous, admission=admission)
