from bridge.psi_witness import detect_generation_conflict, validate_witness


def proof(_: str) -> bool:
    return True


def pointer(generation: int, height: int, state_hash: str, finality_hash: str = "h0"):
    return {
        "epoch": 0,
        "generation": generation,
        "height": height,
        "state_hash": state_hash,
        "finality_height": 0,
        "finality_hash": finality_hash,
    }


def witness():
    return {
        "status": "DECIDED",
        "pi_old": pointer(0, 0, "h0"),
        "pi_new": pointer(1, 1, "h1"),
        "gamma_w": "gamma-w",
        "gamma_f": "gamma-f",
        "omega": "omega",
        "g_old": 0,
        "g_new": 1,
        "token": "t1",
    }


def test_complete_decided_witness_is_authoritative():
    result = validate_witness(witness(), pointer(0, 0, "h0"), verify_proof=proof)
    assert result.status == "CONTINUE"
    assert result.reason_code == "VALID_WITNESS"
    assert result.authoritative is True


def test_prepared_witness_is_aborted_not_authoritative():
    value = witness()
    value["status"] = "PREPARED"
    result = validate_witness(value, pointer(0, 0, "h0"), verify_proof=proof)
    assert result.status == "REPLAY"
    assert result.authoritative is False


def test_missing_decision_context_fails_closed():
    value = witness()
    del value["pi_old"]
    result = validate_witness(value, pointer(0, 0, "h0"), verify_proof=proof)
    assert result.status == "HALT"
    assert result.reason_code == "INCOMPLETE_WITNESS"


def test_old_pointer_mismatch_fails_closed():
    value = witness()
    value["pi_old"] = pointer(0, 0, "fork")
    result = validate_witness(value, pointer(0, 0, "h0"), verify_proof=proof)
    assert result.reason_code == "WITNESS_OLD_STATE_MISMATCH"


def test_generation_gap_fails_closed():
    value = witness()
    value["g_new"] = 2
    result = validate_witness(value, pointer(0, 0, "h0"), verify_proof=proof)
    assert result.reason_code == "WITNESS_GENERATION_GAP"


def test_invalid_gamma_fails_closed():
    value = witness()
    result = validate_witness(value, pointer(0, 0, "h0"), verify_proof=lambda _: False)
    assert result.reason_code == "INVALID_WITNESS_PROOF"


def test_conflicting_authoritative_witnesses_halt():
    first = witness()
    second = witness()
    second["pi_new"] = pointer(1, 1, "fork")
    result = detect_generation_conflict([first, second])
    assert result is not None
    assert result.status == "HALT"
    assert result.reason_code == "CONFLICTING_WITNESS"
