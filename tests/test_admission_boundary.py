"""Regression tests for the explicit semantic admission boundary."""
from __future__ import annotations

import pytest

from core.admission import Admission, admit, require_admitted
from core.evolution import evolutionary_psi_transition
from core.proof import ProofObligation
from core.state import State


def _proof(passed: bool) -> ProofObligation:
    return ProofObligation(
        passed=passed,
        invariant=passed,
        viable=passed,
        evidence={"test": True},
    )


def test_admission_accepts_only_proof_result():
    candidate = State(values={"x": "next", "relations": ()})
    result = admit(candidate, _proof(True))
    assert isinstance(result, Admission)
    assert result.accepted is True
    assert require_admitted(result) is candidate


def test_rejected_admission_cannot_be_required():
    candidate = State(values={"x": "next", "relations": ()})
    result = admit(candidate, _proof(False))
    assert result.accepted is False
    with pytest.raises(ValueError, match="not admitted"):
        require_admitted(result)


def test_admission_requires_explicit_proof_object():
    candidate = State(values={"x": "next", "relations": ()})
    with pytest.raises(TypeError, match="ProofObligation"):
        admit(candidate, True)


def test_canonical_evolution_uses_admission_before_selection():
    def generate(state):
        return (
            state.evolve(values={"x": "a", "relations": ()}),
            state.evolve(values={"x": "b", "relations": ("r",)}),
        )

    transition = evolutionary_psi_transition(
        generate=generate,
        test=lambda _candidate: True,
    )
    result = transition(State(values={"x": "current", "relations": ()}).to_psi())
    assert result.x in {"a", "b"}
