import pytest

from core.canonical_boundary import canonicalize_psi
from core.psi_transition import PsiTransition
from core.state import Psi, State


def test_state_adapter_cannot_be_used_as_canonical_commit_input():
    psi = Psi(x=(1,), relations=())
    adapted = State.from_psi(psi)

    with pytest.raises(TypeError, match="canonical"):
        canonicalize_psi(adapted)


def test_psi_transition_on_state_is_adapter_only():
    transition = PsiTransition(lambda x, r: (x + (2,), r))
    state = State.from_psi(Psi(x=(1,), relations=()))

    adapted = transition.on_state(state)

    assert adapted.to_psi() == Psi(x=(1, 2), relations=())


def test_direct_psi_transition_remains_fundamental():
    transition = PsiTransition(lambda x, r: (x + (2,), r))
    assert transition(Psi(x=(1,), relations=())) == Psi(
        x=(1, 2), relations=()
    )
