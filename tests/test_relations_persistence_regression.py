from core.state import State


def test_relations_persist_through_state_evolution():
    relations = {"r1": "x->y"}
    state = State(values={"x": 1, "relations": relations})

    evolved = state.evolve(x=2)

    assert evolved.values["x"] == 2
    assert evolved.values["relations"] == relations


def test_relations_can_be_explicitly_replaced():
    state = State(values={"x": 1, "relations": {"r1": "x->y"}})
    new_relations = {"r2": "y->z"}

    evolved = state.evolve(relations=new_relations)

    assert evolved.values["relations"] == new_relations
