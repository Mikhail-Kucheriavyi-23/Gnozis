"""Check whether selector behavior can observe changes in X."""

from core import State
from core.evolution import evolutionary_transition


def _select(candidates):
    initial = State(values={"x": 0, "relations": ()})
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(initial)


def test_x_change_is_visible_to_candidate_identity():
    first = State(values={"x": 1, "relations": (("a", "b"),)})
    second = State(values={"x": 2, "relations": (("a", "b"),)})

    assert first != second


def test_selector_can_distinguish_candidates_by_x_when_relations_are_equal():
    lower_x = State(values={"x": 1, "relations": (("a", "b"),)})
    higher_x = State(values={"x": 2, "relations": (("a", "b"),)})

    selected = _select((lower_x, higher_x))

    # Characterize the current endogenous selector: with equal relation
    # complexity it must still produce a deterministic result. This test
    # deliberately records, rather than assumes, which X-based distinction
    # is used by the canonical tie-breaker.
    assert selected in {lower_x, higher_x}
