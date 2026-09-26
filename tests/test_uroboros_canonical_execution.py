from core.history import AppendOnlyHistory
from core.state import State
from core.uroboros import Uroboros


def generate(state):
    base = tuple(state.values.get("x", ()))
    for value in (1, 2):
        values = dict(state.values)
        values["x"] = base + (value,)
        yield State(values=values)


def test_evolutionary_uroboros_uses_legacy_engine_without_canonical_history():
    core = Uroboros.evolutionary(
        generate=generate,
        test=lambda state: True,
        history=AppendOnlyHistory(),
        kernel_version="test-kernel",
    )

    assert core.executor is None
    result = core.step()

    assert result.state.to_psi().x == (1,)
    assert result.executor is None


def test_rejected_uroboros_step_preserves_state_and_history():
    core = Uroboros.evolutionary(
        generate=generate,
        test=lambda state: state.values.get("x") > 999,
        history=AppendOnlyHistory(),
        kernel_version="test-kernel",
    )

    result = core.step()

    assert result.state.to_psi().x == ()
    assert result.executor is None
