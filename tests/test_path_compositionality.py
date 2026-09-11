"""Characterize direct-vs-composed transition behavior without assuming equality."""

from core import State
from core.evolution import evolutionary_transition


def test_composed_path_reaches_declared_terminal_state():
    initial = State(values={"x": 0, "relations": ()})
    middle = State(values={"x": 1, "relations": (("a", "b"),)})
    terminal = State(values={"x": 2, "relations": (("b", "c"),)})

    step_one = evolutionary_transition(lambda _s: (middle,), lambda _c: True)
    step_two = evolutionary_transition(lambda _s: (terminal,), lambda _c: True)

    result = step_two(step_one(initial))

    assert result == terminal
    assert result.values["x"] == 2
    assert result.values["relations"] == (("b", "c"),)


def test_direct_path_is_not_assumed_to_equal_composed_path():
    initial = State(values={"x": 0, "relations": ()})
    middle = State(values={"x": 1, "relations": (("a", "b"),)})
    composed_terminal = State(values={"x": 2, "relations": (("b", "c"),)})
    direct_terminal = State(values={"x": 2, "relations": (("a", "c"),)})

    composed = evolutionary_transition(lambda _s: (middle,), lambda _c: True)(initial)
    composed = evolutionary_transition(lambda _s: (composed_terminal,), lambda _c: True)(composed)
    direct = evolutionary_transition(lambda _s: (direct_terminal,), lambda _c: True)(initial)

    # The current contract does not assert path independence.
    assert composed != direct
    assert composed == composed_terminal
    assert direct == direct_terminal
