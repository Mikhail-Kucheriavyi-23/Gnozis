
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional

from .state import State


Transition = Callable[[State], State]


@dataclass
class Engine:
    """Minimal deterministic transition engine for GNOSIS/UROBOROS."""

    transition: Optional[Transition] = None

    def step(self, state: State) -> State:
        """Apply one endogenous transition to the current state."""
        if self.transition is None:
            return state

        next_state = self.transition(state)

        if not isinstance(next_state, State):
            raise TypeError("transition must return a State instance")

        return next_state

    def run(self, state: State, steps: int) -> State:
        """Evolve a state for a finite number of steps."""
        if steps < 0:
            raise ValueError("steps must be non-negative")

        current = state

        for _ in range(steps):
            current = self.step(current)

        return current

    def iterate(self, state: State, steps: int) -> Iterable[State]:
        """Yield successive states without mutating the input state."""
        if steps < 0:
            raise ValueError("steps must be non-negative")

        current = state

        for _ in range(steps):
            current = self.step(current)
            yield current

