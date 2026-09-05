from core import Engine, Relation, State, Uroboros

def increment(state: State) -> State:
value = state.values.get("value", 0)
return State(values={"value": value + 1})

def test_state_creation():
state = State(values={"value": 1})


assert state.values["value"] == 1


def test_state_is_immutable():
state = State(values={"value": 1})


evolved = state.evolve(values={"value": 2})

assert state.values["value"] == 1
assert evolved.values["value"] == 2
assert state is not evolved


def test_relation_creation():
relation = Relation(
source="a",
target="b",
)


assert relation.source == "a"
assert relation.target == "b"
assert relation.relation_type == "related"


def test_relation_validation():
try:
Relation(
source="a",
target="b",
relation_type="",
)
except ValueError:
pass
else:
raise AssertionError(
"Empty relation_type must raise ValueError."
)

def test_engine_creation():
engine = Engine(transition=increment)


assert engine is not None


def test_engine_step():
state = State(values={"value": 1})
engine = Engine(transition=increment)


next_state = engine.step(state)

assert next_state.values["value"] == 2
assert state.values["value"] == 1


def test_engine_run():
state = State(values={"value": 1})
engine = Engine(transition=increment)


result = engine.run(state, steps=3)

assert result.values["value"] == 4


def test_engine_trajectory():
state = State(values={"value": 1})
engine = Engine(transition=increment)


trajectory = list(engine.trajectory(state, steps=3))

assert [s.values["value"] for s in trajectory] == [1, 2, 3, 4]


def test_uroboros_initialization():
uroboros = Uroboros()


assert uroboros.state is not None
assert uroboros.engine is not None


def test_uroboros_step():
engine = Engine(transition=increment)


uroboros = Uroboros(
    state=State(values={"value": 1}),
    engine=engine,
)

next_uroboros = uroboros.step()

assert next_uroboros.state.values["value"] == 2
assert uroboros.state.values["value"] == 1


def test_uroboros_with_relations():
uroboros = Uroboros()


relations = [
    Relation(source="a", target="b"),
    Relation(source="b", target="c"),
]

configured = uroboros.with_relations(relations)

assert configured.state == uroboros.state
assert configured.engine == uroboros.engine

