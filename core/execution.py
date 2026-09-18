"""Canonical execution owner: pure Psi transition plus proof/admission plus history."""
from __future__ import annotations

from dataclasses import dataclass

from .admission import Admission
from .commit import commit
from .history import AppendOnlyHistory
from .proof import ProofObligation
from .psi_transition import PsiTransition
from .state import Psi


@dataclass(frozen=True)
class ExecutionResult:
    psi: Psi
    history: AppendOnlyHistory


@dataclass
class CanonicalExecutor:
    history: AppendOnlyHistory
    kernel_version: str

    def step(self, psi: Psi, transition: PsiTransition, admission: Admission) -> ExecutionResult:
        if not isinstance(psi, Psi):
            raise TypeError("psi must be Psi.")
        if not isinstance(transition, PsiTransition):
            raise TypeError("transition must be PsiTransition.")
        if not isinstance(admission, Admission):
            raise TypeError("admission must be Admission.")
        if not isinstance(admission.proof, ProofObligation):
            raise TypeError("admission.proof must be ProofObligation.")
        if admission.accepted and admission.candidate != transition(psi):
            raise ValueError("admitted candidate does not match transition result.")
        if not admission.accepted:
            return ExecutionResult(psi=psi, history=self.history)

        committed, history = commit(
            previous=psi,
            admission=admission,
            kernel_version=self.kernel_version,
        ).apply(self.history)
        self.history = history
        return ExecutionResult(psi=committed, history=history)
