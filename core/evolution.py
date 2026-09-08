from __future__ import annotations

from typing import Callable, Iterable

from .state import State

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]
Selector = Callable[[list[State]], State]


def select_next_state(
    state: State,
    generate: Generator,
    test: Tester,
    select: Selector,
) -> State:
    """Endogenous Generate → Test → Select transition.

    Selection is restricted to candidates that have passed the test.
    No external intervention is required between generation and selection.
    """
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")

    valid = [candidate for candidate in candidates if test(candidate)]
    if not valid:
        raise ValueError("No candidate state passed the test")

    chosen = select(valid)
    if chosen not in valid:
        raise ValueError("Selector must choose one of the tested candidates")

    return chosen


def evolutionary_transition(
    generate: Generator,
    test: Tester,
    select: Selector,
) -> Callable[[State], State]:
    """Build an Engine-compatible endogenous evolutionary transition."""
    return lambda state: select_next_state(state, generate, test, select)
