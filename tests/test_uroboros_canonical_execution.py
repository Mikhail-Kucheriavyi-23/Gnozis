from core.history import AppendOnlyHistory
from core.state import State
from core.uroboros import Uroboros


def generate(state):
    values = dict(state.values)
    values["x"] = tuple(values.get("x", ())) + (1,)
    yield State(values=values)


def test_evolutionary_uroboros_uses_canonical_executor_and_history():
    core = Uroboros.evolutionary(
        generate=generate,
        test=lambda state: True,
        history=AppendOnlyHistory(),
        kernel_version="test-kernel",
    )

    assert core.executor is not None
    result = core.step()

    assert result.state.to_psi().x == (1,)
    assert result.executor is core.executor
    assert len(result.executor.history.records) == 1


def test_rejected_uroboros_step_preserves_state_and_history():
    core = Uroboros.evolutionary(
        generate=generate,
        test=lambda state: False,
        history=AppendOnlyHistory(),
        kernel_version="test-kernel",
    )

    result = core.step()

    assert result.state.to_psi().x == ()
    assert result.executor.history.records == ()
