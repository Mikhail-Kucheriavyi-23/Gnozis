import pytest
from core.safety import SafetyGate

def test_default_gate_allows_bounded_operations():
    assert SafetyGate().allows(20)
    assert not SafetyGate().allows(21)

def test_authority_gain_blocks():
    assert not SafetyGate(authority_gain=1).allows(1)

def test_hard_stop_and_silence_block():
    assert not SafetyGate(hard_stop=True).allows(1)
    assert not SafetyGate(silence=True).allows(1)

def test_require_fails_closed():
    with pytest.raises(PermissionError):
        SafetyGate(hard_stop=True).require(1)
