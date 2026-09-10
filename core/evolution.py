from __future__ import annotations

from dataclasses import replace
from typing import Callable, Iterable

from .state import State

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]


def _endogenous_score(state: State) -> tuple[int, str]:
    """Deterministic selection criterion derived only from candidate state.

    Lower complexity (fewer relations) is preferred; ties are resolved by a
    canonical representation. No externally supplied selector is involved.
    """
    return (len(state.relations), repr(state))


def select_next_state(
    state: State,
    generate: Generator,
    test: Tester,
) -> State:
    """Endogenous Generate → Test → Select transition."""
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")

    valid = [candidate for candidate in candidates if test(candidate)]
    if not valid:
        raise ValueError("No candidate state passed the test")

    return min(valid, key=_endogenous_score)


def evolutionary_transition(
    generate: Generator,
    test: Tester,
) -> Callable[[State], State]:
    """Build an Engine-compatible transition with endogenous selection."""
    return lambda state: select_next_state(state, generate, test)
