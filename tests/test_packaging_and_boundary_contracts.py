import pytest

from core import Relation, State


def test_state_rejects_none_relations_at_construction():
    with pytest.raises(TypeError, match="relations must be iterable"):
        State(values={"x": 1}, relations=None)  # type: ignore[arg-type]


def test_state_copies_relation_iterable_container():
    relation = Relation(source="a", target="b")
    supplied = [relation]
    state = State(values={"x": 1}, relations=supplied)

    supplied.clear()

    assert state.relations == (relation,)


def test_evolve_copies_supplied_relation_iterable_container():
    old_relation = Relation(source="a", target="b")
    new_relation = Relation(source="b", target="c")
    state = State(values={"x": 1}, relations=[old_relation])
    supplied = [new_relation]

    evolved = state.evolve(relations=supplied)
    supplied.clear()

    assert evolved.relations == (new_relation,)
    assert state.relations == (old_relation,)
