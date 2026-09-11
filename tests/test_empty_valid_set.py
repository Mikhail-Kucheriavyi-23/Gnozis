"""Contract test: no accepted candidate must not invent a next state."""

import pytest

from core import State
from core.evolution import evolutionary_transition


def test_no_valid_candidate_does_not_invent_state():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})
    rejected_a = State(values={"x": 1, "relations": ()})
    rejected_b = State(values={"x": 2, "relations": (("b", "c"),)})

    transition = evolutionary_transition(
        lambda _state: (rejected_a, rejected_b),
        lambda _candidate: False,
    )

    with pytest.raises(ValueError):
        transition(initial)

    assert initial.values["x"] == 0
    assert initial.values["relations"] == (("a", "b"),)


def test_no_valid_candidate_cannot_fallback_to_a_rejected_candidate():
    initial = State(values={"x": 0, "relations": ()})
    rejected = State(values={"x": 999, "relations": ()})

    transition = evolutionary_transition(
        lambda _state: (rejected,),
        lambda _candidate: False,
    )

    with pytest.raises(ValueError) as error:
        transition(initial)

    assert "valid" in str(error.value).lower()
    assert initial != rejected
