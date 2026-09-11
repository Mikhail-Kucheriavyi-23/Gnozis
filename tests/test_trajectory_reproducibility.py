"""Verify deterministic trajectory selection from the same initial state."""

from core import State
from core.evolution import evolutionary_transition


def _trajectory(initial, candidates_by_x):
    current = initial
    seen = []
    for _ in range(3):
        seen.append(current)
        candidates = candidates_by_x[current.values["x"]]
        current = evolutionary_transition(lambda _s, cs=candidates: cs, lambda _c: True)(current)
    seen.append(current)
    return seen


def test_same_initial_state_and_candidates_reproduce_same_trajectory():
    initial = State(values={"x": 0, "relations": ()})
    a = State(values={"x": 1, "relations": (("a", "b"),)})
    b = State(values={"x": 2, "relations": (("b", "c"),)})
    c = State(values={"x": 3, "relations": ()})

    candidates = {
        0: (a,),
        1: (b,),
        2: (c,),
        3: (c,),
    }

    first = _trajectory(initial, candidates)
    second = _trajectory(initial, candidates)

    assert first == second


def test_trajectory_is_independent_of_candidate_input_order():
    initial = State(values={"x": 0, "relations": ()})
    preferred = State(values={"x": 1, "relations": (("a", "b"),)})
    alternate = State(values={"x": 1, "relations": (("c", "d"),)})
    next_state = State(values={"x": 2, "relations": ()})

    def run(order):
        current = initial
        for _ in range(2):
            candidates = order[current.values["x"]]
            current = evolutionary_transition(lambda _s, cs=candidates: cs, lambda _c: True)(current)
        return current

    ordered = {0: (alternate, preferred), 1: (next_state,), 2: (next_state,)}
    reversed_order = {0: (preferred, alternate), 1: (next_state,), 2: (next_state,)}

    assert run(ordered) == run(reversed_order)
