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
    """Perform one endogenous Generate → Test → Select transition over Ψ.

    Candidates are complete ``State`` values, so an evolution may change the
    X representation, the R representation, or both. The tester is a strict
    boolean boundary and the selector may only return one of the exact tested
    candidate objects.
    """
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")

    for candidate in candidates:
        if not isinstance(candidate, State):
            raise TypeError("Generator must produce State instances")

    valid: list[State] = []
    for candidate in candidates:
        result = test(candidate)
        if not isinstance(result, bool):
            raise TypeError("Tester must return a bool")
        if result:
            valid.append(candidate)

    if not valid:
        raise ValueError("No candidate state passed the test")

    chosen = select(valid)
    if not isinstance(chosen, State):
        raise TypeError("Selector must return a State instance")
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
