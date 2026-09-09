from core.relation import Relation
from core.state import State


def test_state_evolve_preserves_relations_in_fundamental_state():
    relation = Relation("a", "b", "link")
    state = State({"x": {"a": 1}, "relations": (relation,)})

    evolved = state.evolve(values={"x": {"a": 2}, "relations": state.values["relations"]})

    assert evolved.to_psi().relations == (relation,)


def test_state_to_psi_preserves_relations():
    relation = Relation("a", "b", "link")
    state = State({"x": {"a": 1}, "relations": (relation,)})

    psi = state.to_psi()

    assert relation in psi.relations
