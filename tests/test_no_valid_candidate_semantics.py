"""Define the semantic boundary between rejection and an evolution event."""

import pytest

from core import State
from core.evolution import evolutionary_transition


def test_empty_valid_set_is_explicit_non_transition():
    initial = State(values={"x": 0, "relations": ()})

    transition = evolutionary_transition(
        lambda _state: (State(values={"x": 1, "relations": ()}),),
        lambda _candidate: False,
    )

    with pytest.raises(ValueError, match="valid"):
        transition(initial)

    # No accepted candidate means no new state was produced.
    assert initial.values == {"x": 0, "relations": ()}


def test_rejected_candidates_are_not_a_fixed_point():
    initial = State(values={"x": 0, "relations": ()})
    rejected = State(values={"x": 1, "relations": ()})

    transition = evolutionary_transition(
        lambda _state: (rejected,),
        lambda _candidate: False,
    )

    with pytest.raises(ValueError):
        transition(initial)

    assert initial != rejected
