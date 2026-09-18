import pytest

from core.legacy_engine import LegacyEngine
from core.state import Psi, State


def test_legacy_engine_is_not_a_canonical_psi_commit_api():
    state = State.from_psi(Psi(x=(), relations=()))

    def legacy_transition(current: State) -> State:
        return State.from_psi(Psi(x=(1,), relations=()))

    engine = LegacyEngine(transition=legacy_transition)
    changed = engine.step(state)

    assert changed.to_psi() == Psi(x=(1,), relations=())


def test_legacy_transition_can_change_psi_but_is_explicitly_noncanonical():
    """Document the PM-02 reality: the compatibility path can alter semantic
    projection unless callers are prevented from treating it as authority.
    This test must not be interpreted as proof of global no-bypass.
    """
    state = State.from_psi(Psi(x=(), relations=()))

    def legacy_transition(current: State) -> State:
        return State.from_psi(Psi(x=(1,), relations=()))

    changed = LegacyEngine(legacy_transition).step(state)

    assert changed.to_psi().x == (1,)


def test_legacy_engine_has_no_admission_parameter():
    import inspect
    signature = inspect.signature(LegacyEngine)
    assert "admission" not in signature.parameters
