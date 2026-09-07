from __future__ import annotations

from typing import Callable, Iterable

from core import State


Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]
Selector = Callable[[list[State]], State]


def select_next_state(
    state: State,
    generate: Generator,
    test: Tester,
    select: Selector,
) -> State:
    """Generate, test, and select the next state without external intervention."""
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
