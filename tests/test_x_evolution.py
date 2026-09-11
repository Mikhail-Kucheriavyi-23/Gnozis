"""Check that X can evolve while R remains unchanged."""

from core import State
from core.evolution import evolutionary_transition


def test_x_can_evolve_with_fixed_relations():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    candidate = State(values={"x": ("a", "b"), "relations": (("a", "b"),)})

    result = evolutionary_transition(lambda _state: (candidate,), lambda _s: True)(initial)

    assert result.values["x"] != initial.values["x"]
    assert result.to_psi().relations == initial.to_psi().relations


def test_test_can_permit_x_change_while_rejecting_unwanted_relation_change():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    x_only = State(values={"x": ("a", "b"), "relations": (("a", "b"),)})
    x_and_r = State(values={"x": ("a", "b"), "relations": ()})

    def test(candidate):
        return candidate.to_psi().relations == initial.to_psi().relations

    result = evolutionary_transition(lambda _state: (x_and_r, x_only), test)(initial)

    assert result == x_only
    assert result.values["x"] == ("a", "b")
    assert result.to_psi().relations == initial.to_psi().relations
