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


def _generic_score(state: State) -> tuple[str]:
    """Deterministic score for the generic State compatibility path.

    This path is intentionally independent of the canonical Psi=(X,R)
    representation. It therefore must not require State.to_psi().
    """
    return (repr(state),)


def _psi_score(state: State) -> tuple[int, str]:
    """Deterministic endogenous score for canonical Psi evolution."""
    psi = state.to_psi()
    return (len(psi.relations), repr(psi))


def select_next_state(state: State, generate: Generator, test: Tester) -> State:
    """Generic endogenous Generate -> Test -> Select transition."""
    candidates = list(generate(state))
    if not candidates:
        raise ValueError("Generator must produce at least one candidate state")

    valid = [candidate for candidate in candidates if _test_candidate(test, candidate)]
    if not valid:
        raise ValueError("No candidate state passed the test")

    return min(valid, key=_generic_score)


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
        candidates = list(generate(current))
        if not candidates:
            raise ValueError("Generator must produce at least one candidate state")
        valid = [candidate for candidate in candidates if _test_candidate(test, candidate)]
        if not valid:
            raise ValueError("No candidate state passed the test")
        next_state = min(valid, key=_psi_score)
        next_psi = next_state.to_psi()
        return next_psi.x, next_psi.relations

    return PsiTransition(function=transition)
