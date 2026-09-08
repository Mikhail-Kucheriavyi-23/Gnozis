import pytest

from core.state import State


def test_state_does_not_alias_nested_mutable_values():
    source = {"nested": {"items": [1, 2]}}
    state = State(values={"x": 1, "relations": (), "payload": source})

    source["nested"]["items"].append(3)

    assert state.values["payload"]["nested"]["items"] == (1, 2)


def test_state_nested_mutable_values_cannot_be_mutated_through_state():
    state = State(values={"x": 1, "relations": (), "payload": {"items": [1, 2]}})

    with pytest.raises((TypeError, AttributeError)):
        state.values["payload"]["items"].append(3)


def test_evolve_does_not_alias_input_mapping_or_nested_values():
    source = {"items": [1]}
    state = State(values={"x": 1, "relations": (), "payload": source})

    evolved = state.evolve(values={"x": 2, "relations": (), "payload": source})
    source["items"].append(2)

    assert state.values["payload"]["items"] == (1,)
    assert evolved.values["payload"]["items"] == (1,)


def test_state_evolve_returns_distinct_state():
    state = State(values={"x": 1, "relations": ()})
    evolved = state.evolve(values={"x": 2, "relations": ()})

    assert evolved is not state
    assert state.values["x"] == 1
    assert evolved.values["x"] == 2
