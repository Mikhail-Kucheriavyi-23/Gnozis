"""Verify that relation extinction is not a one-off special case."""

from core import State
from core.evolution import evolutionary_transition


def _step(state, candidate):
    return evolutionary_transition(lambda _s: (candidate,), lambda _c: True)(state)


def test_empty_relations_remain_valid_across_multiple_steps():
    state = State(values={"x": 0, "relations": (("a", "b"),)})
    empty = State(values={"x": 1, "relations": ()})
    empty_again = State(values={"x": 2, "relations": ()})

    state = _step(state, empty)
    state = _step(state, empty_again)

    assert state == empty_again
    assert state.values["relations"] == ()


def test_regeneration_after_extinction_does_not_require_nonempty_initial_relations():
    empty = State(values={"x": 0, "relations": ()})
    regenerated = State(values={"x": 1, "relations": (("c", "d"),)})

    result = _step(empty, regenerated)

    assert result == regenerated
    assert result.values["relations"] == (("c", "d"),)
