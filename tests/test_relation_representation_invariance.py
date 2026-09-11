"""Check whether semantically equivalent relation orderings are treated equally."""

from core import State
from core.evolution import evolutionary_transition


def _select(candidates):
    initial = State(values={"x": 0, "relations": ()})
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(initial)


def test_relation_order_is_not_a_hidden_selector_factor_when_semantics_match():
    ordered_a = State(values={"x": 1, "relations": (("a", "b"), ("c", "d"))})
    ordered_b = State(values={"x": 1, "relations": (("c", "d"), ("a", "b"))})

    # Characterize the current contract: both states remain valid and distinct
    # values; this test records whether storage order itself affects selection.
    forward = _select((ordered_a, ordered_b))
    reverse = _select((ordered_b, ordered_a))

    assert forward == reverse


def test_relation_ordered_states_are_not_mutated_during_selection():
    state = State(values={"x": 1, "relations": (("a", "b"), ("c", "d"))})
    before = state.values["relations"]

    _select((state,))

    assert state.values["relations"] == before
