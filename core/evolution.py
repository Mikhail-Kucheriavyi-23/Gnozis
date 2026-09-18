from __future__ import annotations

from typing import Callable, Iterable

from .admission import admit, require_admitted
from .proof import prove_transition
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
    """Deterministic score for the generic State compatibility path."""
    return (repr(state),)


def _psi_score(state: State) -> tuple[int, str]:
    """Deterministic score for canonical Psi evolution."""
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
    """Build the canonical F: Psi -> Psi transition with proof-gated selection.

    Generate produces the candidate pool. ProofObligation independently evaluates
    each candidate against the invariant/test and depth-1 viability. Select only
    receives candidates whose proof passed. No generation or selection occurs in
    the proof layer itself.
    """

    def transition(x: object, relations: object) -> tuple[object, object]:
        current = State.from_psi(Psi(x, relations))
        candidates = list(generate(current))
        if not candidates:
            raise ValueError("Generator must produce at least one candidate state")

        proofs = [
            prove_transition(current, candidate, candidates, test)
            for candidate in candidates
        ]
        admissions = [
            admit(candidate, proof)
            for candidate, proof in zip(candidates, proofs)
        ]
        valid = [
            admission
            for admission in admissions
            if admission.accepted
        ]
        if not valid:
            raise ValueError("No candidate state passed ProofObligation")

        selected = min(
            valid,
            key=lambda admission: _psi_score(require_admitted(admission)),
        )
        next_state = require_admitted(selected)
        next_psi = next_state.to_psi()
        return next_psi.x, next_psi.relations

    return PsiTransition(function=transition)
