import pytest

from core.commit import commit
from core.admission import admit
from core.proof import ProofObligation
from core.state import Psi


def proof(passed):
    return ProofObligation(
        passed=passed,
        invariant=passed,
        viable=passed,
        evidence={"test": True},
    )


def test_only_admitted_psi_can_cross_semantic_commit():
    current = Psi(x=("a",), relations=())
    candidate = Psi(x=("b",), relations=())

    result = commit(current, admit(candidate, proof(True)))
    assert result.apply() == candidate


def test_rejected_candidate_cannot_cross_semantic_commit():
    current = Psi(x=("a",), relations=())
    candidate = Psi(x=("b",), relations=())

    result = commit(current, admit(candidate, proof(False)))
    with pytest.raises(ValueError, match="not admitted"):
        result.apply()


def test_non_psi_candidate_cannot_be_semantic_commit():
    current = Psi(x=("a",), relations=())
    result = commit(current, admit(object(), proof(True)))
    with pytest.raises(TypeError, match="admitted Psi"):
        result.apply()
