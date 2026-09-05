from core import Engine, Relation, State, Uroboros


def increment(state: State) -> State:
    return State(value=state.value + 1)


def test_state_creation():
    state = State(value=1)
    assert state.value == 1


def test_relation_creation():
    relation = Relation(source="a", target="b")
    assert relation.source == "a"
    assert relation.target == "b"


def test_engine_creation():
    engine = Engine()
    assert engine is not None


def test_engine_step():
    state = State(value=1)
    engine = Engine(transform=increment)

    next_state = engine.step(
        state=state,
        relations=(),
    )

    assert next_state.value == 2


def test_uroboros_initialization():
    uroboros = Uroboros()

    assert uroboros.state is not None
    assert uroboros.engine is not None
