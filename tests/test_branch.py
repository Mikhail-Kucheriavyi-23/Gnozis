from core.branch import Branch, incomparable
from core.state import Psi


def test_branch_identity_and_lineage():
    root = Branch(Psi(x=("root",), relations=()))
    left = Branch(Psi(x=("left",), relations=()), parent=root)
    right = Branch(Psi(x=("right",), relations=()), parent=root)

    assert root.is_ancestor_of(left)
    assert root.is_ancestor_of(right)
    assert incomparable(left, right)


def test_ancestor_branches_are_not_incomparable():
    root = Branch(Psi(x=("root",), relations=()))
    child = Branch(Psi(x=("child",), relations=()), parent=root)

    assert not incomparable(root, child)
