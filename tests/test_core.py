from core import Engine, Relation, State, Uroboros


def increment(state: State) -> State:
    return state


def test_state_creation():
    state = State()
    assert state is not None


def test_engine_creation():
    engine = Engine()
    assert engine is not None


def test_relation_creation():
    relation = Relation(source="a", target="b")
    assert relation.source == "a"
    assert relation.target == "b"


def test_uroboros_initialization():
    uroboros = Uroboros()
    assert uroboros is not None


def test_uroboros_step():
    uroboros = Uroboros()
    next_uroboros = uroboros.step()
    assert isinstance(next_uroboros, Uroboros)
