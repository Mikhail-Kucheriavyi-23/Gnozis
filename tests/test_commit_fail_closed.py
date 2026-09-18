import pytest

from core.commit import commit
from core.admission import Admission
from core.proof import ProofObligation
from core.state import Psi


def test_canonical_commit_rejects_unadmitted_candidate():
    previous = Psi(x=(), relations=())
    rejected = Psi(x=(1,), relations=())

    proof = ProofObligation(
        passed=False,
        invariant=False,
        viable=False,
        evidence={"adversarial": True},
    )
    admission = Admission(
        accepted=False,
        candidate=rejected,
        proof=proof,
    )

    with pytest.raises(ValueError, match="not admitted"):
        commit(previous, admission).apply()


def test_canonical_commit_accepts_admitted_psi():
    previous = Psi(x=(), relations=())
    candidate = Psi(x=(1,), relations=())

    proof = ProofObligation(
        passed=True,
        invariant=True,
        viable=True,
        evidence={"test": True},
    )
    admission = Admission(
        accepted=True,
        candidate=candidate,
        proof=proof,
    )

    assert commit(previous, admission).apply() == candidate
