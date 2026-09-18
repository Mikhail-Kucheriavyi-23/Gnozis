"""Canonical admission boundary for semantic state transitions.

Admission is deliberately separate from candidate generation, testing and
selection. A transition may be applied semantically only after this boundary
returns an accepted result.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .proof import ProofObligation


@dataclass(frozen=True)
class Admission:
    """Immutable result of the semantic admission gate."""

    accepted: bool
    candidate: Any
    proof: ProofObligation

    @property
    def evidence(self) -> Mapping[str, Any]:
        return self.proof.evidence


def admit(candidate: Any, proof: ProofObligation) -> Admission:
    """Admit exactly a proof-passing candidate.

    This function does not generate or select candidates. It is the explicit
    boundary between proof evaluation and semantic transition application.
    """
    if not isinstance(proof, ProofObligation):
        raise TypeError("Admission requires a ProofObligation.")
    if type(proof.passed) is not bool:
        raise TypeError("ProofObligation.passed must be bool.")
    return Admission(
        accepted=proof.passed,
        candidate=candidate,
        proof=proof,
    )


def require_admitted(admission: Admission) -> Any:
    """Return the admitted candidate or stop without a semantic mutation."""
    if not isinstance(admission, Admission):
        raise TypeError("semantic transition requires an Admission result.")
    if not admission.accepted:
        raise ValueError("Candidate was not admitted.")
    return admission.candidate
