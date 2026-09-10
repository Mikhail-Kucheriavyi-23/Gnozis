import pytest

from core import Psi, Relation, State


def test_psi_is_the_fundamental_x_r_pair():
    relation = Relation(source="a", target="b")
    psi = Psi(x={"value": 1}, relations=[relation])

    assert psi.x == {"value": 1}
    assert psi.relations == (relation,)


def test_psi_rejects_non_relation_members():
    with pytest.raises(TypeError):
        Psi(x="x", relations=["not-a-relation"])


def test_state_psi_round_trip_preserves_fundamental_state():
    relation = Relation(source="a", target="b")
    state = State(values={"x": {"value": 1}, "relations": [relation]})

    restored = State.from_psi(state.to_psi())

    assert restored.to_psi() == state.to_psi()


def test_state_to_psi_requires_explicit_x_and_relations():
    with pytest.raises(ValueError):
        State(values={"value": 1}).to_psi()
