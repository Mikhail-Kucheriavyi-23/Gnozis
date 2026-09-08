"""Canonical fundamental transition boundary for Psi=(X,R).

Psi is the complete input/output domain of the fundamental dynamics.
State is only an adapter around Psi and may contain derived metadata.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .state import State


@dataclass(frozen=True)
class Psi:
    """Fundamental state: exactly the pair (X, R)."""

    x: Any
    relations: Any

    @classmethod
    def from_state(cls, state: State) -> "Psi":
        return cls(state.values["x"], state.values["relations"])

    def to_state(self) -> State:
        return State(values={"x": self.x, "relations": self.relations})


PsiFunction = Callable[[Any, Any], tuple[Any, Any]]


@dataclass(frozen=True)
class PsiTransition:
    """Canonical fundamental operator F: Psi -> Psi."""

    function: PsiFunction

    def __call__(self, psi: Psi) -> Psi:
        next_x, next_relations = self.function(psi.x, psi.relations)
        return Psi(next_x, next_relations)

    def on_state(self, state: State) -> State:
        """Explicit adapter for legacy State-based engines."""
        return self(Psi.from_state(state)).to_state()


def make_psi_transition(function: PsiFunction) -> PsiTransition:
    """Construct the canonical F: Psi -> Psi operator."""
    return PsiTransition(function=function)
