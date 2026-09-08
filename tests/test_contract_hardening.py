import pytest

from core import Engine, State, Uroboros


def test_engine_rejects_bool_step_count():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="steps must be an integer"):
        engine.run(State(), True)

    with pytest.raises(TypeError, match="steps must be an integer"):
        list(engine.trajectory(State(), False))


def test_engine_accepts_only_real_integer_step_counts():
    engine = Engine(transition=lambda state: state)

    assert engine.run(State(), 0).values == {}
    assert list(engine.trajectory(State(), 0)) == [State()]


def test_uroboros_rejects_bool_step_count():
    core = Uroboros()

    with pytest.raises(TypeError, match="steps must be an integer"):
        core.run(True)


def test_evolve_omitted_component_is_preserved_and_empty_relations_are_explicit():
    from core import Relation

    relation = Relation("a", "b")
    state = State(values={"x": 1}, relations=(relation,))

    value_changed = state.evolve(values={"x": 2})
    relation_cleared = state.evolve(relations=())

    assert value_changed.relations == (relation,)
    assert relation_cleared.values == state.values
    assert relation_cleared.relations == ()
    assert state.relations == (relation,)


def test_evolve_none_is_neither_omitted_nor_empty():
    state = State(values={"x": 1})

    with pytest.raises(TypeError):
        state.evolve(values=None)
    with pytest.raises(TypeError):
        state.evolve(relations=None)


def test_evolve_requires_at_least_one_explicit_component():
    with pytest.raises(TypeError, match="requires values and/or relations"):
        State(values={"x": 1}).evolve()
