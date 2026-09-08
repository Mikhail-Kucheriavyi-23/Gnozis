import pytest

from core import Engine, Relation, State, Uroboros, select_next_state


def increment(state: State) -> State:
    value = state.values.get("value", 0)
    return State(values={"value": value + 1}, relations=state.relations)


def test_state_creation():
    state = State(values={"value": 1})
    assert state.values["value"] == 1


def test_state_nested_values_are_immutable():
    state = State(values={"nested": {"value": 1}, "items": [1, 2]})
    with pytest.raises(TypeError):
        state.values["nested"]["value"] = 2
    assert state.values["items"] == (1, 2)


def test_state_evolve_preserves_unspecified_relations():
    relation = Relation(source="a", target="b")
    state = State(values={"value": 1}, relations=(relation,))
    evolved = state.evolve(values={"value": 2})
    assert evolved.values["value"] == 2
    assert evolved.relations == (relation,)
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
    assert engine.step(state).values["value"] == 2


def test_engine_run():
    state = State(values={"value": 1})
    engine = Engine(transition=increment)
    assert engine.run(state, steps=3).values["value"] == 4


def test_engine_rejects_bool_steps():
    engine = Engine(transition=increment)
    with pytest.raises(TypeError):
        engine.run(State(), steps=True)


def test_engine_trajectory():
    state = State(values={"value": 1})
    engine = Engine(transition=increment)
    trajectory = list(engine.trajectory(state, steps=3))
    assert len(trajectory) == 4
    assert [item.values["value"] for item in trajectory] == [1, 2, 3, 4]


def test_uroboros_initialization():
    uroboros = Uroboros()
    assert uroboros.state is not None
    assert uroboros.engine is not None


def test_uroboros_step():
    uroboros = Uroboros(
        state=State(values={"value": 1}),
        engine=Engine(transition=increment),
    )
    assert uroboros.step().state.values["value"] == 2


def test_uroboros_preserves_relations():
    relation = Relation(source="a", target="b")
    uroboros = Uroboros(state=State(relations=(relation,)))
    configured = uroboros.with_relations([Relation(source="x", target="y")])
    assert uroboros.state.relations == (relation,)
    assert configured.state.relations == (Relation(source="x", target="y"),)


def test_gts_rejects_non_boolean_test_result():
    candidate = State(values={"value": 2})
    with pytest.raises(TypeError):
        select_next_state(
            State(),
            generate=lambda _: [candidate],
            test=lambda _: 1,
            select=lambda candidates: candidates[0],
        )


def test_gts_never_selects_untested_candidate():
    rejected = State(values={"value": 0})
    accepted = State(values={"value": 1})
    calls = []

    def test(candidate: State) -> bool:
        calls.append(candidate.values["value"])
        return candidate.values["value"] == 1

    chosen = select_next_state(
        State(),
        generate=lambda _: [rejected, accepted],
        test=test,
        select=lambda candidates: candidates[0],
    )
    assert chosen == accepted
    assert calls == [0, 1]
