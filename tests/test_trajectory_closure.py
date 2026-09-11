"""Verify closure over a finite accepted evolution trajectory."""

from core import State
from core.evolution import evolutionary_transition


def test_accepted_trajectory_remains_in_state_space():
    states = [
        State(values={"x": 0, "relations": ()}),
        State(values={"x": 1, "relations": (("a", "b"),)}),
        State(values={"x": 2, "relations": (("b", "c"),)}),
        State(values={"x": 3, "relations": ()}),
    ]

    def make_transition(current):
        index = states.index(current)
        if index + 1 >= len(states):
            return evolutionary_transition(lambda _s: (), lambda _c: True)
        nxt = states[index + 1]
        return evolutionary_transition(lambda _s: (nxt,), lambda _c: True)

    current = states[0]
    state_space = {state.values for state in states}

    for _ in range(len(states) - 1):
        current = make_transition(current)(current)
        assert current.values in state_space

    assert current == states[-1]


def test_rejected_candidate_cannot_break_trajectory_closure():
    initial = State(values={"x": 0, "relations": ()})
    valid = State(values={"x": 1, "relations": (("a", "b"),)})
    invalid = State(values={"x": "outside", "relations": None})

    def test(candidate):
        return candidate == valid

    result = evolutionary_transition(lambda _s: (invalid, valid), test)(initial)

    assert result == valid
    assert result.values["x"] == 1
    assert result.values["relations"] == (("a", "b"),)
