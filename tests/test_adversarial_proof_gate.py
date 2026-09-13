"""Adversarial integration checks for the canonical proof-gated evolution path."""

from core.evolution import evolutionary_psi_transition


def _valid_candidate():
    return {"X": {"a", "b"}, "R": {("a", "b")}}


def _invalid_candidate():
    return {"X": {"a"}, "R": {("a", "b")}}


def _dead_end_candidate():
    return {"X": {"a"}, "R": set()}


def test_invalid_candidate_is_rejected():
    result = evolutionary_psi_transition(
        {"X": {"a"}, "R": set()},
        [_invalid_candidate(), _valid_candidate()],
    )
    assert result is not None
    assert result != _invalid_candidate()


def test_dead_end_candidate_does_not_become_next_state():
    result = evolutionary_psi_transition(
        {"X": {"a"}, "R": set()},
        [_dead_end_candidate()],
    )
    assert result is None


def test_empty_candidate_pool_stops():
    result = evolutionary_psi_transition(
        {"X": {"a"}, "R": set()},
        [],
    )
    assert result is None
