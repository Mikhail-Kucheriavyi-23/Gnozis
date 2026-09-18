"""Canonical semantic commit boundary.

PsiTransition computes a candidate Psi. It does not itself mutate semantic
state. Only an admitted, explicitly canonical Psi candidate can cross this
commit boundary.
"""
from __future__ import annotations

from dataclasses import dataclass

from .admission import Admission, require_admitted
from .canonical_boundary import canonicalize_psi
from .state import Psi


@dataclass(frozen=True)
class SemanticCommit:
    previous: Psi
    admission: Admission

    def apply(self) -> Psi:
        candidate = require_admitted(self.admission)
        canonical = canonicalize_psi(candidate)
        return canonical.psi


def commit(previous: Psi, admission: Admission) -> SemanticCommit:
    if not isinstance(previous, Psi):
        raise TypeError("previous must be Psi.")
    return SemanticCommit(previous=previous, admission=admission)
