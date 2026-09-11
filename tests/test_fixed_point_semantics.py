"""Verify that an accepted unchanged candidate is a genuine fixed point."""

from core import State
from core.evolution import evolutionary_transition


def test_accepted_unchanged_candidate_is_fixed_point():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    candidate = State(values={"x": ("a",), "relations": (("a", "b"),)})

    result = evolutionary_transition(lambda _state: (candidate,), lambda _s: True)(initial)

    assert result == initial
    assert result.to_psi() == initial.to_psi()


def test_fixed_point_is_not_rejection():
    initial = State(values={"x": 0, "relations": ()})
    same = State(values={"x": 0, "relations": ()})

    result = evolutionary_transition(lambda _state: (same,), lambda _s: True)(initial)

    assert result == same
    assert result == initial


def test_fixed_point_does_not_mutate_initial_state():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    same = State(values={"x": ("a",), "relations": (("a", "b"),)})
    before = initial.values

    result = evolutionary_transition(lambda _state: (same,), lambda _s: True)(initial)

    assert result.values == before
    assert initial.values == before
