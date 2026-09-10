import pytest

from core import Engine, Relation, State, Uroboros


def increment(state: State) -> State:
    value = state.values.get("value", 0)
    return State(values={"value": value + 1})


def test_state_creation():
    state = State(values={"value": 1})
    assert state.values["value"] == 1


def test_relation_creation():
    relation = Relation(source="a", target="b")
    assert relation.source == "a"
    assert relation.target == "b"


def test_engine_creation():
    engine = Engine(transition=increment)
    assert engine is not None


def test_engine_step():
    state = State(values={"value": 1})
    engine = Engine(transition=increment)
    next_state = engine.step(state)
    assert next_state.values["value"] == 2


def test_engine_run():
    state = State(values={"value": 1})
    engine = Engine(transition=increment)
    result = engine.run(state, steps=3)
    assert result.values["value"] == 4


def test_engine_trajectory():
    state = State(values={"value": 1})
    engine = Engine(transition=increment)
    trajectory = list(engine.trajectory(state, steps=3))
    assert len(trajectory) == 4
    assert [s.values["value"] for s in trajectory] == [1, 2, 3, 4]


def test_uroboros_requires_explicit_engine():
    with pytest.raises(TypeError):
        Uroboros()  # type: ignore[call-arg]


def test_uroboros_step():
    uroboros = Uroboros(
        state=State(values={"value": 1}),
        engine=Engine(transition=increment),
    )
    next_uroboros = uroboros.step()
    assert next_uroboros.state.values["value"] == 2


def test_engine_rejects_bool_steps():
    engine = Engine(transition=increment)
    state = State(values={"value": 1})
    with pytest.raises(TypeError):
        engine.run(state, steps=True)
    with pytest.raises(TypeError):
        list(engine.trajectory(state, steps=False))


def test_engine_rejects_closure_transition():
    offset = 1

    def hidden_transition(state: State) -> State:
        return State(values={"value": state.values.get("value", 0) + offset})

    with pytest.raises(ValueError, match="closure"):
        Engine(transition=hidden_transition)
