from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State


Transition = Callable[[State], State]


def _validate_callable_boundary(value: object, name: str) -> None:
    if not callable(value):
        raise TypeError(f"{name} must be callable")
    closure = getattr(value, "__closure__", None)
    if closure:
        raise ValueError(
            f"{name} must not capture hidden closure state; "
            "pass evolving state explicitly through State."
        )


def _validate_transition(transition: Transition) -> None:
    """Reject a transition whose executable state is hidden in a closure."""
    _validate_callable_boundary(transition, "transition")

    # EvolutionaryTransition stores its generator and tester explicitly.
    # Validate those callables as well without importing the evolution module.
    for name in ("generate", "test"):
        nested = getattr(transition, name, None)
        if nested is not None:
            _validate_callable_boundary(nested, name)


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
