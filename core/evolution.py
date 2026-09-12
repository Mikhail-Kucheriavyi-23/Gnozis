from __future__ import annotations

from typing import Callable, Iterable

from .psi_transition import PsiTransition
from .state import Psi, State

Generator = Callable[[State], Iterable[State]]
Tester = Callable[[State], bool]


def _test_candidate(test: Tester, candidate: State) -> bool:
    """Enforce the fundamental Test(candidate) -> bool contract."""
    result = test(candidate)
    if type(result) is not bool:
        raise TypeError("Test(candidate) must return bool exactly.")
    return result


def _endogenous_score(state: State) -> tuple[int, str]:
    """Deterministic selection criterion derived only from candidate state."""
    psi = state.to_psi()
    return (len(psi.relations), repr(state))


def select_next_state(state: State, generate: Generator, test: Tester) -> State:
    """Endogenous Generate -> Test -> Select transition."""
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")

    valid = [candidate for candidate in candidates if _test_candidate(test, candidate)]
    if not valid:
        raise ValueError("No candidate state passed the test")

    return min(valid, key=_endogenous_score)


def evolutionary_transition(generate: Generator, test: Tester) -> Callable[[State], State]:
    """Build the legacy State-based transition interface."""
    return lambda state: select_next_state(state, generate, test)


def evolutionary_psi_transition(generate: Generator, test: Tester) -> PsiTransition:
    """Build the canonical fundamental F: Psi -> Psi transition.

    Generate/Test remain implementation hooks over the State adapter, but the
    fundamental input and output of the evolution operator are Psi=(X,R).
    No State metadata can become part of the fundamental transition domain.
    """

    def transition(x: object, relations: object) -> tuple[object, object]:
        current = State.from_psi(Psi(x, relations))
        next_state = select_next_state(current, generate, test)
        next_psi = next_state.to_psi()
        return next_psi.x, next_psi.relations

    return PsiTransition(function=transition)
