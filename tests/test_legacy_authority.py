import pytest

from core.legacy_authority import is_canonical_authority, reject_as_canonical
from core.state import Psi, State


def test_legacy_state_is_never_canonical_authority():
    state = State.from_psi(Psi(x=(1,), relations=()))
    assert is_canonical_authority(state) is False


def test_legacy_state_cannot_be_promoted_to_canonical_authority():
    state = State.from_psi(Psi(x=(1,), relations=()))
    with pytest.raises(TypeError, match="compatibility-only"):
        reject_as_canonical(state)
