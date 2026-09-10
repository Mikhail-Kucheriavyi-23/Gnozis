from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .memory import Memory
from .observation import Observation
from .state import Psi


CandidateBuilder = Callable[[Psi, Observation], Psi]
CandidateTest = Callable[[Psi, Psi, Observation], bool]


@dataclass(frozen=True)
class ObservationCycle:
    """Explicit bridge from external observations to Ψ evolution.

    Memory records observations; it never mutates Ψ. A candidate becomes the
    next Ψ only when the supplied test explicitly accepts it.
    """

    memory: Memory
    build_candidate: CandidateBuilder
    test_candidate: CandidateTest

    def ingest(self, psi: Psi, observation: Observation) -> Psi:
        if not isinstance(psi, Psi):
            raise TypeError("psi must be a Psi instance")
        if not isinstance(observation, Observation):
            raise TypeError("observation must be an Observation instance")

        self.memory.remember(observation)
        candidate = self.build_candidate(psi, observation)
        if not isinstance(candidate, Psi):
            raise TypeError("candidate builder must return Psi")

        accepted = self.test_candidate(psi, candidate, observation)
        if type(accepted) is not bool:
            raise TypeError("candidate test must return bool")
        return candidate if accepted else psi
