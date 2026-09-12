import pytest

from core import State


def test_x_and_relations_are_read_only_projections() -> None:
    state = State(values={"x": 1, "relations": (("a", "b"),)})

    assert state.x == 1
    assert state.relations == (("a", "b"),)


def test_missing_projection_is_not_a_second_state_model() -> None:
    state = State(values={"score": 1})

    with pytest.raises(AttributeError):
        _ = state.x
    with pytest.raises(AttributeError):
        _ = state.relations
