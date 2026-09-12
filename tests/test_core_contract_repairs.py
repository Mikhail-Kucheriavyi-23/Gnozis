import pytest

from core import Engine, State, Uroboros
from core.evolution import evolutionary_transition


def increment(state: State) -> State:
    return State(values={"value": state.values.get("value", 0) + 1})


def test_engine_rejects_bool_steps() -> None:
    engine = Engine(transition=increment)
    state = State(values={"value": 0})

    with pytest.raises(TypeError):
        engine.run(state, steps=True)

    with pytest.raises(TypeError):
        list(engine.trajectory(state, steps=False))


def test_test_contract_rejects_truthy_non_bool() -> None:
    transition = evolutionary_transition(
        generate=lambda state: (State(values={"x": 1, "relations": ()}),),
        test=lambda state: "yes",
    )

    with pytest.raises(TypeError, match="must return bool"):
        transition(State(values={"x": 0, "relations": ()}))


def test_unconfigured_uroboros_fails_closed() -> None:
    uroboros = Uroboros(state=State(values={"x": 0, "relations": ()}))

    with pytest.raises(RuntimeError, match="no transition configured"):
        uroboros.step()


def test_uroboros_relations_are_preserved() -> None:
    uroboros = Uroboros(
        state=State(values={"x": 1, "relations": ()}),
        engine=Engine(transition=increment),
    )

    updated = uroboros.with_relations(("a", "b"))

    assert updated.state.values["relations"] == (("a", "b"),)
    assert uroboros.state.values["relations"] == ()
