import pytest

from bridge.gnosis_terminal_bridge import BridgeHalt, CanonicalPointer, GnosisTerminalBridge


def proof(_: str) -> bool:
    return True


def request(**overrides):
    value = {
        "command": "step",
        "epoch": 0,
        "generation": 1,
        "height": 1,
        "provenance": {"h_prev": "h0", "h_next": "h1"},
        "authorization": {"gamma_signature": "gamma", "omega_order": "omega"},
    }
    value.update(overrides)
    return value


def bridge():
    return GnosisTerminalBridge(
        CanonicalPointer(0, 0, 0, "h0", 0, "h0"),
        verify_proof=proof,
    )


def test_valid_continuity_advances_canonical():
    result = bridge().execute("step", request())
    assert result.execution_status == "CONTINUE"
    assert result.reason_code == "CANONICAL_ADVANCED"
    assert result.canonical_pointer.generation == 1
    assert result.canonical_pointer.height == 1
    assert result.canonical_pointer.state_hash == "h1"


def test_generation_reuse_is_rejected():
    b = bridge()
    b.execute("step", request())
    result = b.execute("step", request(generation=1, height=2, provenance={"h_prev": "h1", "h_next": "h2"}))
    assert result.execution_status == "REJECT"
    assert result.reason_code == "GENERATION_FENCE_MISMATCH"


def test_broken_provenance_is_rejected():
    result = bridge().execute(
        "step", request(provenance={"h_prev": "fork", "h_next": "h1"})
    )
    assert result.execution_status == "REJECT"
    assert result.reason_code == "PROVENANCE_DISCONTINUITY"


def test_invalid_certificate_is_rejected():
    def reject(_: str) -> bool:
        return False

    b = GnosisTerminalBridge(
        CanonicalPointer(0, 0, 0, "h0", 0, "h0"),
        verify_proof=reject,
    )
    result = b.execute("step", request())
    assert result.execution_status == "REJECT"
    assert result.reason_code == "INVALID_GAMMA"


def test_finality_conflict_halts():
    b = bridge()
    b.execute("step", request(authorization={
        "gamma_signature": "gamma",
        "omega_order": "omega",
        "gamma_finality": "final-1",
    }))
    with pytest.raises(BridgeHalt):
        b.execute("step", request(
            generation=2,
            height=2,
            provenance={"h_prev": "h1", "h_next": "h2"},
            authorization={
                "gamma_signature": "gamma",
                "omega_order": "omega",
                "gamma_finality": "final-2",
            },
        ))


def test_prepared_witness_is_not_authoritative():
    result = bridge().recover([
        {"status": "PREPARED", "g_old": 0, "token": "x", "pi_new": {}}
    ])
    assert result.execution_status == "REPLAY"
    assert result.canonical_pointer.generation == 0


def test_decided_witness_replays():
    result = bridge().recover([
        {
            "status": "DECIDED",
            "g_old": 0,
            "token": "x",
            "pi_new": {
                "epoch": 0,
                "generation": 1,
                "height": 1,
                "state_hash": "h1",
                "finality_height": 0,
                "finality_hash": "h0",
            },
        }
    ])
    assert result.execution_status == "REPLAY"
    assert result.canonical_pointer.generation == 1
    assert result.canonical_pointer.state_hash == "h1"
