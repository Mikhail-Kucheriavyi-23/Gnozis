from __future__ import annotations

from typing import Callable

from .state import Psi, State

PsiTransition = Callable[[Psi], Psi]


def apply_psi_transition(state: State, transition: PsiTransition) -> State:
    """Apply a fundamental Psi=(X,R) transition through the State adapter."""
    psi = state.to_psi()
    next_psi = transition(psi)
    if not isinstance(next_psi, Psi):
        raise TypeError("Psi transition must return Psi")
    return State.from_psi(next_psi)
