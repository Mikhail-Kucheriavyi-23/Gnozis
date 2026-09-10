from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .psi_transition import PsiTransition
from .state import Psi, State

Transition = Callable[[State], State]


@dataclass
class Engine:
    """Deterministic transition engine with a canonical Ψ=(X,R) boundary."""

    transition: Transition | None = None
    psi_transition: PsiTransition | None = None

    def __post_init__(self) -> None:
        if (self.transition is None) == (self.psi_transition is None):
            raise ValueError("Engine requires exactly one transition boundary")

    @classmethod
    def from_psi(cls, transition: PsiTransition) -> "Engine":
        """Create an Engine whose fundamental transition is Ψ -> Ψ."""
        return cls(psi_transition=transition)

    def step(self, state: State) -> State:
        """Apply one transition, adapting through Ψ when configured."""
        if self.psi_transition is not None:
            return self.psi_transition.on_state(state)
        assert self.transition is not None
        next_state = self.transition(state)
        if not isinstance(next_state, State):
            raise TypeError("Engine transition must return a State instance.")
        return next_state

    def step_psi(self, psi: Psi) -> Psi:
        """Apply the canonical Ψ -> Ψ transition without a State round-trip."""
        if self.psi_transition is None:
            if self.transition is None:
                raise RuntimeError("Engine has no transition")
            return self.transition(State.from_psi(psi)).to_psi()
        return self.psi_transition(psi)

    def run(self, state: State, steps: int) -> State:
        if steps < 0:
            raise ValueError("steps must be non-negative.")
        current = state
        for _ in range(steps):
            current = self.step(current)
        return current

    def trajectory(self, state: State, steps: int) -> Iterable[State]:
        if steps < 0:
            raise ValueError("steps must be non-negative.")
        current = state
        yield current
        for _ in range(steps):
            current = self.step(current)
            yield current
