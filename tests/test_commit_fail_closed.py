import pytest

from core.commit import commit
from core.admission import Admission
from core.state import Psi


def test_canonical_commit_rejects_unadmitted_candidate():
    previous = Psi(x=(), relations=())
    rejected = Psi(x=(1,), relations=())

    # Construct the smallest rejected admission object without bypassing
    # the public commit boundary.
    admission = Admission(
        candidate=rejected,
        accepted=False,
        reason="adversarial-test",
    )

    with pytest.raises(Exception):
        commit(previous, admission).apply()


def test_canonical_commit_accepts_admitted_psi():
    previous = Psi(x=(), relations=())
    candidate = Psi(x=(1,), relations=())

    admission = Admission(
        candidate=candidate,
        accepted=True,
        reason="test",
    )

    assert commit(previous, admission).apply() == candidate
