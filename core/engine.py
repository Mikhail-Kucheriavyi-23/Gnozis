from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State


Transition = Callable[[State], State]


def _validate_transition(transition: Transition) -> None:
    """Reject transitions that capture hidden runtime state in a closure.

    The core transition contract is State -> State. Closure-captured values
    would make the next state depend on state outside the explicit input.
    Callable objects are allowed when their state is explicit in the object
    itself and can therefore be inspected/tested as part of the engine.
    """
    if not callable(transition):
        raise TypeError("transition must be callable")

    closure = getattr(transition, "__closure__", None)
    if closure:
        raise ValueError(
            "Engine transition must not capture hidden closure state; "
            "pass all evolving state explicitly through State."
        )


@dataclass
class Engine:
    """Deterministic State -> State transition engine."""

    transition: Transition

    def __post_init__(self) -> None:
        _validate_transition(self.transition)

    def step(self, state: State) -> State:
        """Apply one transition to the current state."""
        next_state = self.transition(state)

        if not isinstance(next_state, State):
            raise TypeError("Engine transition must return a State instance.")

        return next_state

    @staticmethod
    def _validate_steps(steps: int) -> None:
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
