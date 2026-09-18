import pytest

from core.meta_transition import MetaTransition, RefinementProof
from core.root_invariant import RootInvariant


def test_refinement_predicate_is_required_when_supplied():
    root = RootInvariant(lambda k: k["sealed"])
    before = {"sealed": True, "v": 1}
    after = {"sealed": True, "v": 2}
    proof = RefinementProof(
        root, before, after, "preserves K0", refinement=lambda a, b: b["v"] > a["v"]
    )
    assert MetaTransition(before, after, proof).admissible()


def test_failed_refinement_blocks_meta_transition():
    root = RootInvariant(lambda k: k["sealed"])
    before = {"sealed": True, "v": 2}
    after = {"sealed": True, "v": 1}
    proof = RefinementProof(
        root, before, after, "claimed refinement", refinement=lambda a, b: b["v"] > a["v"]
    )
    transition = MetaTransition(before, after, proof)
    assert not transition.admissible()
    with pytest.raises(ValueError, match="not admitted"):
        transition.apply()
