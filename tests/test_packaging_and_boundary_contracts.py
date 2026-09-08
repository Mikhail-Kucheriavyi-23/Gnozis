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


def test_evolve_preserves_r_when_only_x_changes_after_external_relation_list_mutation():
    relation = Relation(source="a", target="b")
    state = State(values={"x": 1}, relations=[relation])
    replacement = [Relation(source="b", target="c")]

    evolved = state.evolve(values={"x": 2})
    replacement.clear()

    assert evolved.values["x"] == 2
    assert evolved.relations == (relation,)
    assert state.relations == (relation,)
