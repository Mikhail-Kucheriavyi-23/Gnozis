import pytest

from core.admission import Admission
from core.execution import CanonicalExecutor
from core.history import AppendOnlyHistory
from core.proof import ProofObligation
from core.psi_transition import PsiTransition
from core.state import Psi


def proof(passed: bool) -> ProofObligation:
    return ProofObligation(
        passed=passed,
        invariant=passed,
        viable=passed,
        evidence={"test": True},
    )


def test_accepted_step_creates_exactly_one_history_record():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    candidate = transition(psi)
    admission = Admission(True, candidate, proof(True))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition, admission)

    assert result.psi == candidate
    assert len(result.history.records) == 1
    assert result.history.records[0].admitted is True


def test_rejected_step_does_not_create_history_record():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    admission = Admission(False, transition(psi), proof(False))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition, admission)

    assert result.psi == psi
    assert result.history.records == ()


def test_admitted_candidate_cannot_disagree_with_transition():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    forged = Psi(x=(999,), relations=())
    admission = Admission(True, forged, proof(True))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    with pytest.raises(ValueError, match="does not match"):
        executor.step(psi, transition, admission)
