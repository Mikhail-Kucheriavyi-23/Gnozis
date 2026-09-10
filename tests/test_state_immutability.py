import pytest

from core.state import State


def test_state_freezes_nested_builtin_containers():
    source = {
        "x": 1,
        "relations": (("a", "b"),),
        "meta": {"items": [1, {"nested": 2}], "tags": {"a", "b"}},
    }
    state = State(values=source)

    with pytest.raises(TypeError):
        state.values["meta"] = {}
    with pytest.raises(TypeError):
        state.values["meta"]["items"] = ()
    with pytest.raises(TypeError):
        state.values["meta"]["items"][1]["nested"] = 3

    assert state.values["meta"]["items"] == (1, {"nested": 2})
    assert state.values["meta"]["tags"] == frozenset({"a", "b"})


def test_mutating_original_input_cannot_mutate_state():
    source = {"x": 1, "relations": (), "meta": {"items": [1]}}
    state = State(values=source)

    source["meta"]["items"].append(2)
    source["x"] = 99

    assert state.values["meta"]["items"] == (1,)
    assert state.values["x"] == 1


def test_evolve_returns_independent_immutable_state():
    state = State(values={"x": 1, "relations": ()})
    evolved = state.evolve(values={"x": 2, "relations": ()})

    assert state.values["x"] == 1
    assert evolved.values["x"] == 2
    assert state is not evolved
