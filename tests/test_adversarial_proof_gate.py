"""Adversarial integration checks for the canonical proof-gated evolution path."""

import pytest

from core.evolution import evolutionary_psi_transition
from core.state import State


def _valid_candidate(label="valid"):
    return State(values={"x": label, "relations": (("a", "b"),)})


def _invalid_candidate():
    return State(values={"x": "invalid", "relations": ()})


def _transition(generate, test=lambda _candidate: True):
    return evolutionary_psi_transition(generate=generate, test=test)


def test_invalid_candidate_is_rejected_when_valid_continuations_exist():
    transition = _transition(
        lambda _state: (
            _invalid_candidate(),
            _valid_candidate("valid-a"),
            _valid_candidate("valid-b"),
        ),
        test=lambda candidate: isinstance(candidate.values["x"], str)
        and candidate.values["x"] != "invalid"
        and isinstance(candidate.values["relations"], tuple),
    )
    result = transition(State(values={"x": "current", "relations": ()}).to_psi())
    assert result.x in {"valid-a", "valid-b"}


def test_dead_end_candidate_is_rejected_by_proof_gate():
    transition = _transition(lambda _state: (_valid_candidate(),))
    with pytest.raises(ValueError, match="ProofObligation"):
        transition(State(values={"x": "current", "relations": ()}).to_psi())


def test_empty_candidate_pool_stops_at_transition_execution():
    transition = _transition(lambda _state: ())
    with pytest.raises(ValueError, match="at least one candidate"):
        transition(State(values={"x": "current", "relations": ()}).to_psi())
