"""Deterministic replay contract over genesis and accepted transition history."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .history import AppendOnlyHistory, TransitionRecord
from .state import Psi

TransitionApplier = Callable[[Psi, TransitionRecord], Psi]


@dataclass(frozen=True)
class ReplayResult:
    state: Psi
    applied: int


def replay(
    genesis: Psi,
    history: AppendOnlyHistory,
    apply: TransitionApplier,
) -> ReplayResult:
    if apply is None or not callable(apply):
        raise TypeError("replay requires an explicit transition applier.")
    state = genesis
    for record in history.records:
        state = apply(state, record)
    return ReplayResult(state=state, applied=len(history.records))
