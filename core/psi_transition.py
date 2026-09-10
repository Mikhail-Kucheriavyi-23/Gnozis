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
        next_x, next_relations = self.function(psi.x, psi.relations)
        return Psi(next_x, next_relations)

    def on_state(self, state: State) -> State:
        """Explicit adapter for State-based engines."""
        return State.from_psi(self(State.to_psi(state)))


def make_psi_transition(function: PsiFunction) -> PsiTransition:
    """Construct the canonical F: Psi -> Psi operator."""
    return PsiTransition(function=function)
