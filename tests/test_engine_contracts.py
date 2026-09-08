import pytest

from core import Engine, State, Uroboros


def test_engine_run_validates_state_even_for_zero_steps():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="Engine.run requires a State instance"):
        engine.run(object(), steps=0)  # type: ignore[arg-type]


def test_engine_trajectory_validates_state_before_first_yield():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="Engine.trajectory requires a State instance"):
        list(engine.trajectory(object(), steps=0))  # type: ignore[arg-type]


def test_uroboros_rejects_invalid_structural_inputs():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="Uroboros.state must be a State instance"):
        Uroboros(state=object(), engine=engine)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="Uroboros.engine must be an Engine instance"):
        Uroboros(state=State(), engine=object())  # type: ignore[arg-type]
