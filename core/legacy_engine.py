"""Explicit compatibility engine for legacy State -> State transitions.

This module is intentionally outside the canonical Ψ semantic surface.
Canonical Ψ code must use PsiEngine/PsiTransition.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State

LegacyTransition = Callable[[State], State]


@dataclass
class LegacyEngine:
    transition: LegacyTransition

    def step(self, state: State) -> State:
        next_state = self.transition(state)
        if not isinstance(next_state, State):
            raise TypeError("Legacy transition must return State.")
        return next_state

    def run(self, state: State, steps: int) -> State:
        if type(steps) is not int:
            raise TypeError("steps must be an int.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")
        current = state
        for _ in range(steps):
            current = self.step(current)
        return current

    def trajectory(self, state: State, steps: int) -> Iterable[State]:
        if type(steps) is not int:
            raise TypeError("steps must be an int.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")
        current = state
        yield current
        for _ in range(steps):
            current = self.step(current)
            yield current
