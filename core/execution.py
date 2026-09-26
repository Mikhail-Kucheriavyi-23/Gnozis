"""Canonical execution owner: Generate -> Proof -> Admission -> Select -> Commit -> History."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .admission import admit
from .commit import commit
from .history import AppendOnlyHistory
from .proof import prove_transition
from .psi_transition import PsiTransition
from .state import Psi, State

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]


@dataclass(frozen=True)
class ExecutionResult:
    psi: Psi
    history: AppendOnlyHistory


@dataclass
class CanonicalExecutor:
    history: AppendOnlyHistory
    kernel_version: str

    def step(
        self,
        psi: Psi,
        transition: PsiTransition,
        *,
        test: Tester | None = None,
    ) -> ExecutionResult:
        """Own a complete canonical Psi execution step."""
        if not isinstance(psi, Psi):
            raise TypeError("psi must be Psi.")
        if not isinstance(transition, PsiTransition):
            raise TypeError("transition must be PsiTransition.")

        candidate = transition(psi)
        current = State.from_psi(psi)
        next_state = State.from_psi(candidate)

        if test is None:
            test = lambda _: True

        # Canonical candidate source is exclusively the declared ΨTransition.
        # The proof is bound to this exact candidate; no alternate candidate
        # source may enter the admission path.
        proof = prove_transition(
            current,
            next_state,
            [next_state],
            test,
        )
        admission = admit(next_state, proof)
        if not admission.accepted:
            return ExecutionResult(psi=psi, history=self.history)

        committed, history = commit(
            previous=psi,
            admission=admission,
            kernel_version=self.kernel_version,
        ).apply(self.history)
        self.history = history
        return ExecutionResult(psi=committed, history=history)

    def evolve(
        self,
        psi: Psi,
        generate: Generator,
        test: Tester,
    ) -> ExecutionResult:
        """Own one complete canonical evolution step."""
        if not isinstance(psi, Psi):
            raise TypeError("psi must be Psi.")

        current = State.from_psi(psi)
        candidates = list(generate(current))
        if not candidates:
            raise ValueError("Generator must produce at least one candidate state")

        proofs = [
            prove_transition(current, candidate, candidates, test)
            for candidate in candidates
        ]
        admissions = [
            admit(candidate, proof)
            for candidate, proof in zip(candidates, proofs)
        ]
        valid = [item for item in admissions if item.accepted]
        # Rejected candidates are terminal at this boundary: they are never
        # transformed, repaired, re-admitted, or exposed to selection.

        if not valid:
            return ExecutionResult(psi=psi, history=self.history)

        selected = min(
            valid,
            key=lambda item: (
                len(item.candidate.to_psi().relations),
                repr(item.candidate.to_psi()),
            ),
        )

        committed, history = commit(
            previous=psi,
            admission=selected,
            kernel_version=self.kernel_version,
        ).apply(self.history)

        self.history = history
        return ExecutionResult(psi=committed, history=history)
