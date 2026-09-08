from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State


Transition = Callable[[State], State]


@dataclass
class Engine:
    """Deterministic state-transition engine for GNOSIS/UROBOROS."""

    transition: Transition

    def step(self, state: State) -> State:
        """Apply one transition to the current state."""
        if not isinstance(state, State):
            raise TypeError("Engine step requires a State instance.")

        next_state = self.transition(state)

        if not isinstance(next_state, State):
            raise TypeError(
                "Engine transition must return a State instance."
            )

        return next_state

    def run(self, state: State, steps: int) -> State:
        """Apply the transition repeatedly for a finite number of steps."""
        if not isinstance(state, State):
            raise TypeError("Engine run requires a State instance.")
        if type(steps) is not int:
            raise TypeError("steps must be an int.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")

        current = state

        for _ in range(steps):
            current = self.step(current)

        return current

    def trajectory(
        self,
        state: State,
        steps: int,
    ) -> Iterable[State]:
        """Yield the initial state followed by each subsequent state."""
        if not isinstance(state, State):
            raise TypeError("Engine trajectory requires a State instance.")
        if type(steps) is not int:
            raise TypeError("steps must be an int.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")

        current = state
        yield current

        for _ in range(steps):
            current = self.step(current)
            yield current
