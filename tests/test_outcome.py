import pytest

from core.branch import Branch
from core.outcome import ParallelOutcome, parallel
from core.state import Psi


def test_parallel_outcome_requires_incomparable_branches():
    root = Branch(Psi(x=("root",), relations=()))
    left = Branch(Psi(x=("left",), relations=()), parent=root)
    right = Branch(Psi(x=("right",), relations=()), parent=root)

    result = parallel(left, right)
    assert isinstance(result, ParallelOutcome)
    assert result.branches == (left, right)


def test_parallel_outcome_rejects_ancestor_pair():
    root = Branch(Psi(x=("root",), relations=()))
    child = Branch(Psi(x=("child",), relations=()), parent=root)

    with pytest.raises(ValueError, match="incomparable"):
        parallel(root, child)
