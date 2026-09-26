"""Canonical fundamental transition boundary for Psi=(X,R).

Psi is the complete input/output domain of the fundamental dynamics.
State is an adapter around Psi and may contain derived metadata.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .state import Psi, State


PsiFunction = Callable[[Any, Any], tuple[Any, Any]]


@dataclass(frozen=True)
class PsiTransition:
    """Canonical fundamental operator F: Psi -> Psi."""

    function: PsiFunction

    def __call__(self, psi: Psi) -> Psi:
        if not isinstance(psi, Psi):
            raise TypeError("PsiTransition requires a Psi input.")
        result = self.function(psi.x, psi.relations)
        if not isinstance(result, tuple) or len(result) != 2:
            raise TypeError("PsiTransition function must return exactly (X, R).")
        next_x, next_relations = result
        return Psi(next_x, next_relations)

    def on_state(self, state: State) -> State:
        """Explicit compatibility adapter: State -> Psi -> State."""
        if not isinstance(state, State):
            raise TypeError("State adapter requires a State input.")
        psi = state.to_psi()
        next_psi = self(psi)
        return State.from_psi(next_psi)


def make_psi_transition(function: PsiFunction) -> PsiTransition:
    """Construct the canonical F: Psi -> Psi operator."""
    return PsiTransition(function=function)
