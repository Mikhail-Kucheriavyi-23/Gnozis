import pytest

from core import Engine, State


def test_engine_rejects_non_state_input():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="Engine step requires a State instance"):
        engine.step({"value": 1})


def test_engine_rejects_non_state_transition_result():
    engine = Engine(transition=lambda state: {"value": 1})

    with pytest.raises(TypeError, match="Engine transition must return a State instance"):
        engine.step(State(values={"value": 0}))


def test_engine_run_rejects_bool_as_step_count():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="steps must be an int"):
        engine.run(State(values={}), True)


def test_engine_trajectory_is_state_only_and_includes_initial_state():
    engine = Engine(
        transition=lambda state: State(values={"value": state.values.get("value", 0) + 1})
    )

    trajectory = list(engine.trajectory(State(values={"value": 0}), 2))

    assert all(isinstance(state, State) for state in trajectory)
    assert [state.values["value"] for state in trajectory] == [0, 1, 2]
