from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .state import State

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]


def _endogenous_score(state: State) -> tuple[int, str]:
    """Deterministic selection criterion derived only from candidate state."""
    return (len(state.values.get("relations", ())), repr(state))


def select_next_state(
    state: State,
    generate: Generator,
    test: Tester,
) -> State:
    """Endogenous Generate -> Test -> Select transition."""
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")

    valid: list[State] = []
    for candidate in candidates:
        if not isinstance(candidate, State):
            raise TypeError("Generator must produce State instances")
        result = test(candidate)
        if not isinstance(result, bool):
            raise TypeError("Test must return bool")
        if result:
            valid.append(candidate)

    if not valid:
        raise ValueError("No candidate state passed the test")

    return min(valid, key=_endogenous_score)


@dataclass(frozen=True)
class EvolutionaryTransition:
    """Explicit callable carrying evolution functions as configuration."""

    generate: Generator
    test: Tester

    def __call__(self, state: State) -> State:
        return select_next_state(state, self.generate, self.test)


def evolutionary_transition(
    generate: Generator,
    test: Tester,
) -> EvolutionaryTransition:
    """Build an explicit Engine-compatible endogenous transition."""
    return EvolutionaryTransition(generate=generate, test=test)
