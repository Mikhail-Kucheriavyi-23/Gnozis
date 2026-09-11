"""Check that relation evolution can occur without arbitrary X replacement."""

from core import State
from core.evolution import evolutionary_transition


def test_relation_evolution_preserves_x_when_candidate_does_not_change_it():
    initial = State(values={"x": ("a", "b"), "relations": (("a", "b"),)})
    candidate = State(values={"x": ("a", "b"), "relations": ()})

    result = evolutionary_transition(lambda _state: (candidate,), lambda _s: True)(initial)

    assert result.values["x"] == initial.values["x"]
    assert result.to_psi().relations == ()


def test_relation_change_is_not_hidden_x_replacement():
    initial = State(values={"x": ("a", "b"), "relations": (("a", "b"),)})
    relation_change = State(values={"x": ("a", "b"), "relations": (("b", "c"),)})
    x_change = State(values={"x": ("changed",), "relations": ()})

    def test(candidate):
        return candidate.values["x"] == initial.values["x"]

    result = evolutionary_transition(
        lambda _state: (x_change, relation_change), test
    )(initial)

    assert result == relation_change
    assert result.values["x"] == initial.values["x"]
    assert result.to_psi().relations == (("b", "c"),)
