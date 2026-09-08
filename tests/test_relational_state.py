from core.engine import Engine
from core.state import State


def relational_transition(state: State) -> State:
    relations = state.values.get("relations", ())
    connected = ("a", "b") in relations
    return state.evolve(
        values={
            **state.values,
            "x": 1 if connected else 0,
        }
    )


def test_relation_can_causally_change_state_without_changing_engine_contract():
    engine = Engine(transition=relational_transition)

    state_a = State(values={"x": 0, "relations": (("a", "b"),)})
    state_b = State(values={"x": 0, "relations": (("a", "c"),)})

    next_a = engine.step(state_a)
    next_b = engine.step(state_b)

    assert next_a.values["x"] == 1
    assert next_b.values["x"] == 0
    assert next_a != next_b


def test_empty_relations_preserve_non_relational_behavior():
    engine = Engine(transition=relational_transition)
    state = State(values={"x": 0, "relations": ()})

    next_state = engine.step(state)

    assert next_state.values["x"] == 0
    assert next_state.values["relations"] == ()


def test_relation_is_preserved_across_state_evolution():
    state = State(values={"x": 0, "relations": (("a", "b"),)})

    next_state = relational_transition(state)

    assert next_state.values["relations"] == (("a", "b"),)
    assert state.values["x"] == 0
    assert next_state.values["x"] == 1
