"""A state-minimal transition boundary for Psi=(X,R).

The transition function receives only the fundamental projection (X, R).
It never receives the mutable/extended State object, so auxiliary metadata
cannot become an implicit input to the fundamental dynamics.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .state import State

Psi = tuple[Any, Any]
PsiFunction = Callable[[Any, Any], Psi]


@dataclass(frozen=True)
class PsiTransition:
    """Transition whose only explicit runtime input is (X, R)."""

    function: PsiFunction

    def __call__(self, state: State) -> State:
        x = state.values["x"]
        relations = state.values["relations"]
        next_x, next_relations = self.function(x, relations)
        return State(values={"x": next_x, "relations": next_relations})


def make_psi_transition(function: PsiFunction) -> PsiTransition:
    """Construct a transition through the minimal Psi=(X,R) boundary."""
    return PsiTransition(function=function)
