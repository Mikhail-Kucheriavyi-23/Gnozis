"""Canonical engine for the fundamental Psi=(X,R) dynamics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .psi_transition import PsiTransition
from .state import Psi


@dataclass(frozen=True)
class PsiEngine:
    """Engine whose only state domain is Psi and whose transition is F: Psi -> Psi."""

    transition: PsiTransition

    def step(self, psi: Psi) -> Psi:
        """Apply exactly one canonical Psi transition."""
        if not isinstance(psi, Psi):
            raise TypeError("PsiEngine.step requires a Psi instance.")
        result = self.transition(psi)
        if not isinstance(result, Psi):
            raise TypeError("PsiEngine transition must return a Psi instance.")
        return result

    def run(self, psi: Psi, steps: int) -> Psi:
        """Apply the canonical transition repeatedly."""
        if type(steps) is not int:
            raise TypeError("steps must be an int, not bool or another numeric type.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")
        current = psi
        for _ in range(steps):
            current = self.step(current)
        return current

    def trajectory(self, psi: Psi, steps: int) -> Iterable[Psi]:
        """Yield Psi states without introducing a second state model."""
        if type(steps) is not int:
            raise TypeError("steps must be an int, not bool or another numeric type.")
        if steps < 0:
            raise ValueError("steps must be non-negative.")
        current = psi
        yield current
        for _ in range(steps):
            current = self.step(current)
            yield current
