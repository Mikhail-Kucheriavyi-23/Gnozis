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
engine = Engine(
transition=lambda state: state
)
assert engine is not None

def test_engine_step():
state = State(values={"value": 1})
engine = Engine(
transition=increment
)


next_state = engine.step(state)

assert next_state.values["value"] == 2


def test_uroboros_initialization():
uroboros = Uroboros()


assert uroboros.state is not None
assert uroboros.engine is not None


def test_uroboros_step():
uroboros = Uroboros(
state=State(values={"value": 1}),
engine=Engine(
transition=increment
),
)


next_uroboros = uroboros.step()

assert next_uroboros.state.values["value"] == 2

