"""Verify selector invariance under candidate enumeration order."""

from itertools import permutations

from core import State
from core.evolution import evolutionary_transition


def test_selection_is_invariant_to_candidate_permutation():
    initial = State(values={"x": 0, "relations": ()})
    candidates = (
        State(values={"x": 1, "relations": (("z", "q"),)}),
        State(values={"x": 1, "relations": (("a", "b"),)}),
        State(values={"x": 1, "relations": (("m", "n"),)}),
    )
    results = []
    for ordered in permutations(candidates):
        transition = evolutionary_transition(lambda _s, cs=ordered: cs, lambda _c: True)
        results.append(transition(initial))
    assert all(result == results[0] for result in results)


def test_selector_does_not_use_candidate_position_as_tiebreaker():
    initial = State(values={"x": 0, "relations": ()})
    first = State(values={"x": 1, "relations": (("a", "b"),)})
    second = State(values={"x": 1, "relations": (("c", "d"),)})
    forward = evolutionary_transition(lambda _s: (first, second), lambda _c: True)(initial)
    reverse = evolutionary_transition(lambda _s: (second, first), lambda _c: True)(initial)
    assert forward == reverse
