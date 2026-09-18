import pytest

from core.meta_transition import MetaTransition, RefinementProof
from core.root_invariant import RootInvariant


def root():
    return RootInvariant(lambda k: k.get("sealed") is True)


def test_valid_meta_transition_requires_k0_proof():
    before = {"sealed": True, "version": 1}
    after = {"sealed": True, "version": 2}
    proof = RefinementProof(root(), before, after, "K0 remains true")
    transition = MetaTransition(before, after, proof)

    assert transition.admissible()
    assert transition.apply() == after


def test_meta_transition_rejects_root_break():
    before = {"sealed": True}
    after = {"sealed": False}
    proof = RefinementProof(root(), before, after, "attempted change")
    transition = MetaTransition(before, after, proof)

    assert not transition.admissible()
    with pytest.raises(ValueError, match="not admitted"):
        transition.apply()


def test_meta_transition_rejects_mismatched_proof():
    before = {"sealed": True, "version": 1}
    after = {"sealed": True, "version": 2}
    wrong_after = {"sealed": True, "version": 3}
    proof = RefinementProof(root(), before, wrong_after, "mismatch")
    transition = MetaTransition(before, after, proof)

    assert not transition.admissible()
