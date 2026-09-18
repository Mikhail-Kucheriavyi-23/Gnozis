from core.branch import Branch
from core.merge import Conflict, merge
from core.state import Psi


def test_identical_branches_merge_without_conflict():
    psi = Psi(x=("a",), relations=())
    branch = Branch(psi)
    result = merge(branch, branch)
    assert result.compatible
    assert result.candidate == psi
    assert result.conflicts == ()


def test_nonidentical_branches_retain_branch_lineage():
    root = Branch(Psi(x=("root",), relations=()))
    left = Branch(Psi(x=("a",), relations=()), parent=root)
    right = Branch(Psi(x=("b",), relations=()), parent=root)
    result = merge(left, right)
    assert not result.compatible
    assert result.candidate is None
    conflict = result.conflicts[0]
    assert isinstance(conflict, Conflict)
    assert conflict.left.branch_id == left.branch_id
    assert conflict.right.branch_id == right.branch_id
    assert conflict.source_psis == (left.psi, right.psi)
