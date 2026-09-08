from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State


Transition = Callable[[State], State]


@dataclass
class Engine:
    """Endogenous state-transition engine for GNOSIS/UROBOROS."""

    transition: Transition

    def step(self, state: State) -> State:
        """Apply one transition to the current state."""
        next_state = self.transition(state)
        if not isinstance(next_state, State):
            raise TypeError("Engine transition must return a State instance.")
        return next_state

    @staticmethod
    def _validate_steps(steps: int) -> None:
        """Reject booleans and non-integral step counts explicitly."""
        if isinstance(steps, bool) or not isinstance(steps, int):
            raise TypeError("steps must be an integer, not bool or another type.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")

    def run(self, state: State, steps: int) -> State:
        """Apply the transition repeatedly for a finite number of steps."""
        self._validate_steps(steps)
        current = state
        for _ in range(steps):
            current = self.step(current)
        return current

    def trajectory(self, state: State, steps: int) -> Iterable[State]:
        """Yield the initial state followed by each subsequent state."""
        self._validate_steps(steps)
        current = state
        yield current
        for _ in range(steps):
            current = self.step(current)
            yield current
