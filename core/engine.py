from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State


Transition = Callable[[State], State]


@dataclass
class Engine:
    """State-transition engine for GNOSIS/UROBOROS."""

    transition: Transition

    def __post_init__(self) -> None:
        if not callable(self.transition):
            raise TypeError("Engine transition must be callable.")

    def step(self, state: State) -> State:
        """Apply one transition to the current State."""
        if not isinstance(state, State):
            raise TypeError("Engine.step requires a State instance.")

        next_state = self.transition(state)

        if not isinstance(next_state, State):
            raise TypeError(
                "Engine transition must return a State instance."
            )

        return next_state

    def run(self, state: State, steps: int) -> State:
        """Apply the transition repeatedly for a finite number of steps."""
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
        """Yield the initial State followed by each subsequent State."""
        if steps < 0:
            raise ValueError("steps must be non-negative.")

        current = state
        yield current

        for _ in range(steps):
            current = self.step(current)
            yield current
