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
    """Endogenous Generate → Test → Select transition over complete State.

    Because State carries both components of Ψ, a generated candidate may
    evolve X, R, or both. Selection remains internal to the GTS transition.
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
