import pytest

from core.merge import Conflict
from core.resolution import ResolutionCandidate, resolve
from core.state import Psi


def test_resolution_produces_candidate_without_mutation():
    left = Psi(x=("a",), relations=())
    right = Psi(x=("b",), relations=())
    conflict = Conflict(left=left, right=right, reason="different")
    candidate = Psi(x=("a", "b"), relations=())
    result = resolve(conflict, candidate, "explicit reconciliation", kernel_version="test-kernel")
    assert isinstance(result, ResolutionCandidate)
    assert result.candidate == candidate
    assert result.source_branches == (left, right)


def test_resolution_requires_explicit_rationale():
    left = Psi(x=("a",), relations=())
    right = Psi(x=("b",), relations=())
    conflict = Conflict(left=left, right=right, reason="different")
    with pytest.raises(ValueError):
        resolve(conflict, Psi(x=("a", "b"), relations=()), "", kernel_version="test-kernel")


def test_resolution_does_not_accept_non_psi_candidate():
    left = Psi(x=("a",), relations=())
    right = Psi(x=("b",), relations=())
    conflict = Conflict(left=left, right=right, reason="different")
    with pytest.raises(TypeError):
        resolve(conflict, object(), "explicit", kernel_version="test-kernel")
