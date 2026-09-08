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

    Only generated State objects that pass the test enter the selection
    boundary. The selector must return the exact tested candidate object,
    preserving candidate lineage rather than merely an equal-by-value copy.
    """
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")
    if not all(isinstance(candidate, State) for candidate in candidates):
        raise TypeError("Generator must produce only State candidates")

    valid = [candidate for candidate in candidates if test(candidate)]
    if not valid:
        raise ValueError("No candidate state passed the test")

    chosen = select(valid)
    if not isinstance(chosen, State):
        raise TypeError("Selector must return a State candidate")
    if not any(chosen is candidate for candidate in valid):
        raise ValueError("Selector must choose one of the tested candidates")

    return chosen


def evolutionary_transition(
    generate: Generator,
    test: Tester,
    select: Selector,
) -> Callable[[State], State]:
    """Build an Engine-compatible endogenous evolutionary transition."""
    return lambda state: select_next_state(state, generate, test, select)
