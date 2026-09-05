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


def test_relation_creation():
relation = Relation(source="a", target="b")


assert relation.source == "a"
assert relation.target == "b"
assert relation.relation_type == "related"


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


final_state = engine.run(state, steps=3)

assert final_state.values["value"] == 4


def test_engine_trajectory():
state = State(values={"value": 1})
engine = Engine(transition=increment)


trajectory = list(engine.trajectory(state, steps=2))

assert [item.values["value"] for item in trajectory] == [1, 2, 3]


def test_uroboros_initialization():
uroboros = Uroboros()


assert uroboros.state is not None
assert uroboros.engine is not None


def test_uroboros_step():
uroboros = Uroboros(
state=State(values={"value": 1}),
engine=Engine(transition=increment),
)


next_uroboros = uroboros.step()

assert next_uroboros.state.values["value"] == 2


