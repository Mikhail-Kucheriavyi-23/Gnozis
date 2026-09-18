import pytest

from core.branch import Branch
from core.merge import Conflict
from core.proof import ProofObligation
from core.resolution import (
    DeferredConflict,
    admit_resolution,
    commit_resolution,
    defer,
    resolve,
)
from core.state import Psi


def proof(passed: bool) -> ProofObligation:
    return ProofObligation(
        passed=passed,
        invariant=passed,
        viable=passed,
        evidence={"test": True},
    )


def conflict():
    root = Branch(Psi(x=("root",), relations=()))
    return Conflict(
        left=Branch(Psi(x=("a",), relations=()), parent=root),
        right=Branch(Psi(x=("b",), relations=()), parent=root),
        reason="different",
    )


def test_deferred_conflict_preserves_both_branches():
    result = defer(conflict(), "insufficient evidence")
    assert isinstance(result, DeferredConflict)
    assert result.conflict.left.psi.x == ("a",)
    assert result.conflict.right.psi.x == ("b",)


def test_resolution_commit_requires_admitted_matching_candidate():
    c = conflict()
    resolution = resolve(c, Psi(x=("a", "b"), relations=()), "explicit reconciliation")
    admission = admit_resolution(resolution, proof(True))
    committed = commit_resolution(c.left.psi, resolution, admission)
    assert committed.apply() == resolution.candidate


def test_rejected_resolution_cannot_commit():
    c = conflict()
    resolution = resolve(c, Psi(x=("a", "b"), relations=()), "explicit reconciliation")
    admission = admit_resolution(resolution, proof(False))
    committed = commit_resolution(c.left.psi, resolution, admission)
    with pytest.raises(ValueError, match="not admitted"):
        committed.apply()
