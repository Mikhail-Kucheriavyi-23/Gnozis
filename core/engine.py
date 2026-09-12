from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .psi_transition import PsiTransition
from .state import State


Transition = Callable[[State], State] | PsiTransition


def _validate_steps(steps: int) -> None:
    """Require a real integer step count; bool is intentionally rejected."""
    if type(steps) is not int:
        raise TypeError("steps must be an int, not bool or another numeric type.")
    if steps < 0:
        raise ValueError("steps must be non-negative.")


@dataclass
class Engine:
    """Deterministic state-transition engine for GNOSIS/UROBOROS."""

    transition: Transition

    def step(self, state: State) -> State:
        """Apply one transition to the current state.

        PsiTransition is the canonical fundamental path. A State callable is
        retained as an explicit compatibility boundary for existing clients.
        """
        if isinstance(self.transition, PsiTransition):
            next_state = self.transition.on_state(state)
        else:
            next_state = self.transition(state)

        if not isinstance(next_state, State):
            raise TypeError("Engine transition must return a State instance.")

        return next_state

    def run(self, state: State, steps: int) -> State:
        """Apply the transition repeatedly for a finite number of steps."""
        _validate_steps(steps)
        current = state
        for _ in range(steps):
            current = self.step(current)
        return current

    def trajectory(self, state: State, steps: int) -> Iterable[State]:
        """Yield the initial state followed by each subsequent state."""
        _validate_steps(steps)
        current = state
        yield current
        for _ in range(steps):
            current = self.step(current)
            yield current
