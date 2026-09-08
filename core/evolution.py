from __future__ import annotations

from typing import Callable, Iterable

from .state import State

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]
Selector = Callable[[list[State]], State]


def select_next_state(state: State, generate: Generator, test: Tester, select: Selector) -> State:
    """Endogenous Generate → Test → Select transition."""
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")
    if not all(isinstance(candidate, State) for candidate in candidates):
        raise TypeError("Generator must produce only State candidates")

    valid = []
    for candidate in candidates:
        result = test(candidate)
        if type(result) is not bool:
            raise TypeError("Test operator must return bool")
        if result:
            valid.append(candidate)

    if not valid:
        raise ValueError("No candidate state passed the test")

    chosen = select(valid)
    if not isinstance(chosen, State):
        raise TypeError("Selector must return a State candidate")
    if not any(chosen is candidate for candidate in valid):
        raise ValueError("Selector must choose one of the tested candidates")
    return chosen


def evolutionary_transition(generate: Generator, test: Tester, select: Selector) -> Callable[[State], State]:
    """Build an Engine-compatible endogenous evolutionary transition."""
    return lambda state: select_next_state(state, generate, test, select)
