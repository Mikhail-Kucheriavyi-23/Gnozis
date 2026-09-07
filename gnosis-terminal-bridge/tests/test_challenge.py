from src.gnosis_terminal_bridge import GnosisTerminalBridge


def test_challenge_is_bound_to_context():
    bridge = GnosisTerminalBridge()

    request = {
        "epoch": 1,
        "generation": 2,
        "height": 1,
    }

    result = bridge.initiate_challenge(request)

    assert result["status"] == "CHALLENGE_ISSUED"

    challenge = result["challenge"]

    assert challenge["epoch"] == 1
    assert challenge["generation"] == 2
    assert challenge["height"] == 1


def test_replay_is_rejected():
    bridge = GnosisTerminalBridge()

    context = {
        "epoch": 1,
        "generation": 2,
        "height": 1,
    }

    result = bridge.initiate_challenge(context)
    challenge = result["challenge"]

    first = bridge.verify_challenge(
        challenge["challenge_id"],
        challenge["value"],
        1,
        2,
        1,
    )

    assert first["status"] == "VERIFIED"

    second = bridge.verify_challenge(
        challenge["challenge_id"],
        challenge["value"],
        1,
        2,
        1,
    )

    assert second["status"] == "REJECT"
    assert second["reason"] == "CHALLENGE_ALREADY_USED"


def test_context_mismatch_is_rejected():
    bridge = GnosisTerminalBridge()

    context = {
        "epoch": 1,
        "generation": 2,
        "height": 1,
    }

    result = bridge.initiate_challenge(context)
    challenge = result["challenge"]

    result = bridge.verify_challenge(
        challenge["challenge_id"],
        challenge["value"],
        1,
        999,
        1,
    )

    assert result["status"] == "REJECT"
    assert result["reason"] == "CONTEXT_MISMATCH"
