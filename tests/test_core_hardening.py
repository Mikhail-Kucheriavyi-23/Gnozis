from dataclasses import FrozenInstanceError

import pytest

from core import Engine, Relation, State


def test_relation_rejects_invalid_relation_type():
    with pytest.raises(TypeError, match="relation_type must be a string"):
        Relation(source="a", target="b", relation_type=None)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="relation_type must not be empty"):
        Relation(source="a", target="b", relation_type="")


def test_state_nested_tuple_and_set_containers_are_structurally_protected():
    state = State(
        values={
            "tuple": (1, {"items": [2]}),
            "set": {1, 2},
        }
    )

    assert state.values["tuple"][1]["items"] == [2]
    assert isinstance(state.values["set"], frozenset)

    with pytest.raises(TypeError, match="immutable sequence"):
        state.values["tuple"][1]["items"].append(3)

    with pytest.raises(AttributeError):
        state.values["set"].add(3)


def test_engine_transition_cannot_mutate_state_owned_mapping():
    state = State(values={"x": 1})

    def transition(current):
        current.values["x"] = 2
        return current

    with pytest.raises(TypeError, match="immutable mapping"):
        Engine(transition=transition).step(state)

    assert state.values["x"] == 1


def test_state_and_relation_outer_assignments_are_rejected():
    state = State(values={"x": 1})
    relation = Relation(source="a", target="b")

    with pytest.raises(FrozenInstanceError):
        state.values = {}  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        state.relations = ()  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        relation.source = "changed"  # type: ignore[misc]


def test_evolve_from_generator_copies_relations_and_preserves_old_state():
    old = Relation(source="a", target="b")
    new = Relation(source="b", target="c")
    state = State(values={"x": 1}, relations=(old,))

    supplied = (relation for relation in [new])
    evolved = state.evolve(relations=supplied)

    assert evolved.relations == (new,)
    assert state.relations == (old,)


def test_explicit_empty_relations_are_distinct_from_omitted_relations():
    relation = Relation(source="a", target="b")
    state = State(values={"x": 1}, relations=(relation,))

    preserved = state.evolve(values={"x": 2})
    emptied = state.evolve(relations=())

    assert preserved.relations == (relation,)
    assert emptied.relations == ()
    assert state.relations == (relation,)
