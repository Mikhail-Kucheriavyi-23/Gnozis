"""Check that the endogenous selector is sensitive to relation structure."""

from core import State
from core.evolution import evolutionary_transition


def _select(candidates):
    initial = State(values={"x": 0, "relations": ()})
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(initial)


def test_relation_structure_can_change_selection():
    sparse = State(values={"x": 1, "relations": (("a", "b"),)})
    dense = State(
        values={
            "x": 1,
            "relations": (("a", "b"), ("b", "c"), ("c", "d")),
        }
    )

    selected_with_sparse = _select((sparse, dense))
    selected_with_dense = _select((dense, sparse))

    assert selected_with_sparse == min((sparse, dense), key=lambda state: repr(state))
    assert selected_with_dense == min((dense, sparse), key=lambda state: repr(state))


def test_relation_change_is_visible_to_candidate_identity():
    first = State(values={"x": 1, "relations": (("a", "b"),)})
    second = State(values={"x": 1, "relations": (("a", "c"),)})

    assert first != second
