import pytest

from core.psi_dynamics import apply_psi_transition
from core.state import Psi, State


def test_psi_transition_roundtrip_preserves_fundamental_state():
    state = State(values={"x": 1, "relations": ("r1",)})

    next_state = apply_psi_transition(
        state,
        lambda psi: Psi(psi.x + 1, psi.relations),
    )

    assert next_state.to_psi() == Psi(2, ("r1",))


def test_psi_transition_cannot_return_arbitrary_state():
    state = State(values={"x": 1, "relations": ()})

    with pytest.raises(TypeError):
        apply_psi_transition(state, lambda psi: state)
