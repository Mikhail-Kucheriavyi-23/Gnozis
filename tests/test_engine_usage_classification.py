from core.engine import Engine
from core.state import State


def test_generic_engine_is_not_canonical_psi_evidence() -> None:
    def transition(state: State) -> State:
        return state.evolve(values={"x": state.values.get("x", 0) + 1})

    result = Engine(transition=transition).step(State(values={"x": 0}))

    assert result.values["x"] == 1
    assert isinstance(result, State)
