from core.relation import Relation
from core.state import State


def test_state_evolve_preserves_relations():
    relation = Relation("a", "b", "link")
    state = State({"a": 1}, relations=(relation,))

    evolved = state.evolve(b=2)

    assert evolved.relations == (relation,)


def test_state_to_psi_preserves_relations():
    relation = Relation("a", "b", "link")
    state = State({"a": 1}, relations=(relation,))

    psi = state.to_psi()

    assert relation in psi.relations
