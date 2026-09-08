from core import State


def test_state_freezes_nested_mutable_containers():
    source = {
        "items": [1, {"nested": [2, 3]}],
        "tags": {"a", "b"},
    }

    state = State(values=source)

    source["items"].append(4)
    source["items"][1]["nested"].append(5)
    source["tags"].add("c")

    assert state.values["items"] == (1, {"nested": (2, 3)})
    assert state.values["tags"] == frozenset({"a", "b"})


def test_state_evolve_does_not_alias_input_containers():
    values = {"items": [1, 2]}
    state = State(values=values)
    values["items"].append(3)

    assert state.values["items"] == (1, 2)


def test_state_evolve_can_explicitly_clear_relations():
    state = State(values={"x": 1}, relations=())
    evolved = state.evolve(values={"x": 2}, relations=())

    assert evolved.relations == ()
