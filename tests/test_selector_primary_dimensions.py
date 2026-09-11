"""Characterize which state dimensions drive the current endogenous selector."""

from core import State
from core.evolution import evolutionary_transition


def _select(candidates):
    initial = State(values={"x": 0, "relations": ()})
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(initial)


def test_relation_count_is_primary_observable_in_current_selector():
    simple = State(values={"x": 1, "relations": (("a", "b"),)})
    complex_state = State(
        values={
            "x": 1,
            "relations": (("a", "b"), ("b", "c")),
        }
    )

    assert _select((complex_state, simple)) == simple


def test_x_does_not_override_relation_count_in_current_selector():
    fewer_relations = State(values={"x": 999, "relations": (("a", "b"),)})
    more_relations = State(
        values={
            "x": -999,
            "relations": (("a", "b"), ("b", "c")),
        }
    )

    assert _select((more_relations, fewer_relations)) == fewer_relations


def test_equal_relation_count_uses_candidate_representation_for_tie_breaking():
    first = State(values={"x": 1, "relations": (("a", "b"),)})
    second = State(values={"x": 2, "relations": (("a", "b"),)})

    selected_forward = _select((first, second))
    selected_reverse = _select((second, first))

    assert selected_forward == selected_reverse
