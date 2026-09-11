"""Verify relation extinction and regeneration are ordinary transitions."""

from core import State
from core.evolution import evolutionary_transition


def test_relations_can_evolve_to_empty_set():
    initial = State(values={"x": 1, "relations": (("a", "b"), ("b", "c"))})
    empty = State(values={"x": 1, "relations": ()})
    transition = evolutionary_transition(lambda _s: (empty,), lambda _c: True)
    assert transition(initial) == empty


def test_empty_relation_set_can_evolve_again():
    empty = State(values={"x": 1, "relations": ()})
    regenerated = State(values={"x": 2, "relations": (("c", "d"),)})
    transition = evolutionary_transition(lambda _s: (regenerated,), lambda _c: True)
    assert transition(empty) == regenerated
