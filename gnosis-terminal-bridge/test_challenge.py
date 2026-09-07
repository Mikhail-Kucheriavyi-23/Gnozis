#!/usr/bin/env python3
"""Minimal interactive challenge/response test for the Gnosis terminal bridge.

This is an M0 protocol test only. It does not create a real cryptographic
credential and must not be used as production authentication.
"""

from gnosis_terminal_bridge import GnosisTerminalBridge


def main() -> None:
    bridge = GnosisTerminalBridge(ttl_seconds=120)

    context = {
        "epoch": 1,
        "generation": 2,
        "height": 1,
    }

    request = {
        "command": "inject",
        **context,
        "provenance": {
            "h_prev": "hash_1",
            "h_next": "challenge_request_hash",
        },
        "authorization": {
            "gamma": "pending_ephemeral_challenge",
            "omega": "request_auth_token",
        },
        "metadata": {
            "action": "INITIATE_CHALLENGE_RESPONSE",
            "target_branch": "feature/gnosis-terminal-bridge",
        },
    }

    issued = bridge.initiate_challenge(request)
    challenge = issued["challenge"]

    print("GNOZIS CHALLENGE")
    print("-----------------")
    print(f"Challenge: {challenge['value']}")
    print(f"Challenge ID: {challenge['challenge_id']}")
    print(f"Epoch: {challenge['epoch']}")
    print(f"Generation: {challenge['generation']}")
    print(f"Height: {challenge['height']}")
    print(f"Expires at: {challenge['expires_at']}")
    print()

    response = input("Enter the six-digit challenge: ").strip()

    verified = bridge.verify_challenge(
        challenge_id=challenge["challenge_id"],
        response=response,
        epoch=context["epoch"],
        generation=context["generation"],
        height=context["height"],
    )

    print("\nVERIFICATION")
    print("------------")
    print(verified)

    # M0 replay test: the same challenge must not be accepted twice.
    replay = bridge.verify_challenge(
        challenge_id=challenge["challenge_id"],
        response=response,
        epoch=context["epoch"],
        generation=context["generation"],
        height=context["height"],
    )

    print("\nREPLAY TEST")
    print("-----------")
    print(replay)


if __name__ == "__main__":
    main()
