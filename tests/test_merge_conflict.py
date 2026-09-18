from core.merge import Conflict, merge
from core.state import Psi


def test_identical_branches_merge_without_conflict():
    psi = Psi(x=("a",), relations=())
    result = merge(psi, psi)
    assert result.compatible
    assert result.candidate == psi
    assert result.conflicts == ()


def test_nonidentical_branches_are_retained_as_conflict():
    left = Psi(x=("a",), relations=())
    right = Psi(x=("b",), relations=())
    result = merge(left, right)
    assert not result.compatible
    assert result.candidate is None
    assert len(result.conflicts) == 1
    assert isinstance(result.conflicts[0], Conflict)
    assert result.conflicts[0].left == left
    assert result.conflicts[0].right == right
