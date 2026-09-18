import pytest

from core.canonical_boundary import CanonicalPsiInput, canonicalize_psi, commit_canonical
from core.state import Psi, State


def test_explicit_psi_crosses_canonical_boundary():
    psi = Psi(x=(1,), relations=())
    assert commit_canonical(psi) == psi


def test_canonical_wrapper_crosses_boundary():
    psi = Psi(x=(1,), relations=())
    wrapped = CanonicalPsiInput(psi)
    assert commit_canonical(wrapped) == psi


def test_legacy_state_cannot_cross_canonical_boundary_implicitly():
    state = State.from_psi(Psi(x=(1,), relations=()))
    with pytest.raises(TypeError, match="cannot cross the canonical"):
        canonicalize_psi(state)


def test_arbitrary_value_cannot_cross_canonical_boundary():
    with pytest.raises(TypeError, match="must be Psi"):
        canonicalize_psi({"x": (1,)})
