import pytest

from core.canonical_chain import admit_transition
from core.history import AppendOnlyHistory, TransitionRecord
from core.provenance import Provenance
from core.safety import SafetyGate


def rec():
    return TransitionRecord(0, "", "s0", "k1", "c0", True, "e0")


def prov():
    return Provenance("c0", "e0", "k1")


def test_canonical_chain_requires_safety_gas_provenance_and_commit():
    result = admit_transition(
        AppendOnlyHistory(), rec(), prov(), "before", "after", 2, (1, 2)
    )
    assert result.applied
    assert result.value == "after"
    assert result.history.head.state_hash == "s0"


def test_canonical_chain_fails_before_commit_on_bad_provenance():
    with pytest.raises(ValueError, match="evidence"):
        admit_transition(
            AppendOnlyHistory(), rec(), Provenance("c0", "wrong", "k1"),
            "before", "after", 1, (1,)
        )


def test_canonical_chain_respects_hard_stop():
    with pytest.raises(PermissionError):
        admit_transition(
            AppendOnlyHistory(), rec(), prov(), "before", "after", 1, (1,),
            SafetyGate(hard_stop=True)
        )


def test_canonical_chain_respects_gas_limit():
    with pytest.raises(ValueError, match="exhausted"):
        admit_transition(
            AppendOnlyHistory(), rec(), prov(), "before", "after", 2, (15, 6),
            gas_limit=20
        )
