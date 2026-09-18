"""Canonical execution owner: Generate -> Proof -> Admission -> Select -> Commit -> History."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .admission import admit
from .commit import commit
from .history import AppendOnlyHistory
from .proof import prove_transition
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

        if not valid:
            return ExecutionResult(psi=psi, history=self.history)

        selected = min(
            valid,
            key=lambda item: (
                len(item.candidate.to_psi().relations),
                repr(item.candidate.to_psi()),
            ),
        )
        candidate_psi = selected.candidate.to_psi()

        committed, history = commit(
            previous=psi,
            admission=admit(candidate_psi, selected.proof),
            kernel_version=self.kernel_version,
        ).apply(self.history)

        self.history = history
        return ExecutionResult(psi=committed, history=history)
