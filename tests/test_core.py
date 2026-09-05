from core import Engine, Relation, State, Uroboros


def test_state_is_immutable():
    state = State(values={"x": 1})

    evolved = state.evolve(values={"x": 2})

    assert state.values["x"] == 1
    assert evolved.values["x"] == 2


def test_engine_step():
    engine = Engine(
        transition=lambda state: state.evolve(
            values={"x": state.values["x"] + 1}
        )
    )

    state = State(values={"x": 0})
    result = engine.step(state)

    assert result.values["x"] == 1


def test_engine_run():
    engine = Engine(
        transition=lambda state: state.evolve(
            values={"x": state.values["x"] + 1}
        )
    )

    state = State(values={"x": 0})
    result = engine.run(state, 5)

    assert result.values["x"] == 5


def test_engine_trajectory():
    engine = Engine(
        transition=lambda state: state.evolve(
            values={"x": state.values["x"] + 1}
        )
    )

    state = State(values={"x": 0})
    trajectory = list(engine.trajectory(state, 3))

    assert [item.values["x"] for item in trajectory] == [0, 1, 2, 3]


def test_relation_creation():
    relation = Relation(source="a", target="b")

    assert relation.source == "a"
    assert relation.target == "b"


def test_uroboros_initialization():
    uroboros = Uroboros()

    assert uroboros is not None
