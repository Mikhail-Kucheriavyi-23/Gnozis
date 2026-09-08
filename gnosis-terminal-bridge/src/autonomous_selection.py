from __future__ import annotations

from typing import Callable, Iterable

from core import State
from core.evolution import select_next_state as _core_select_next_state

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]
Selector = Callable[[list[State]], State]


def select_next_state(
    state: State,
    generate: Generator,
    test: Tester,
    select: Selector,
) -> State:
    """Bridge-compatible entry point delegating to the canonical core GTS."""
    return _core_select_next_state(state, generate, test, select)
