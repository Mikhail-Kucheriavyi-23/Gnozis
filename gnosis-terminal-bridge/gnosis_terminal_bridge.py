import hashlib
import json
import secrets
import time
from dataclasses import dataclass, asdict


@dataclass
class Challenge:
    challenge_id: str
    value: str
    epoch: int
    generation: int
    height: int
    expires_at: int
    used: bool = False


class GnosisTerminalBridge:
    def __init__(self, ttl_seconds: int = 120):
        self.ttl_seconds = ttl_seconds
        self.challenges = {}

    @staticmethod
    def hash_payload(payload: dict) -> str:
        raw = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()
        return hashlib.sha256(raw).hexdigest()

    def initiate_challenge(self, request: dict) -> dict:
        epoch = request["epoch"]
        generation = request["generation"]
        height = request["height"]

        challenge_id = secrets.token_hex(16)
        value = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = int(time.time()) + self.ttl_seconds

        challenge = Challenge(
            challenge_id=challenge_id,
            value=value,
            epoch=epoch,
            generation=generation,
            height=height,
            expires_at=expires_at,
        )
        self.challenges[challenge_id] = challenge

        return {
            "status": "CHALLENGE_ISSUED",
            "challenge": asdict(challenge),
        }

    def verify_challenge(
        self,
        challenge_id: str,
        response: str,
        epoch: int,
        generation: int,
        height: int,
    ) -> dict:
        challenge = self.challenges.get(challenge_id)

        if challenge is None:
            return {"status": "REJECT", "reason": "UNKNOWN_CHALLENGE"}

        if challenge.used:
            return {"status": "REJECT", "reason": "CHALLENGE_ALREADY_USED"}

        if int(time.time()) > challenge.expires_at:
            return {"status": "REJECT", "reason": "CHALLENGE_EXPIRED"}

        if (
            challenge.epoch != epoch
            or challenge.generation != generation
            or challenge.height != height
        ):
            return {"status": "REJECT", "reason": "CONTEXT_MISMATCH"}

        if not secrets.compare_digest(response, challenge.value):
            return {"status": "REJECT", "reason": "INVALID_RESPONSE"}

        challenge.used = True

        return {
            "status": "VERIFIED",
            "agency": {
                "type": "EPHEMERAL",
                "epoch": epoch,
                "generation": generation,
                "height": height,
                "expires_at": challenge.expires_at,
            },
        }


# A long-running bridge must keep one bridge instance so a challenge issued
# by one request can be verified by the following request in the same process.
_BRIDGE = GnosisTerminalBridge()


def handle(request: dict) -> dict:
    command = request.get("command")

    if command == "inject":
        action = request.get("metadata", {}).get("action")

        if action == "INITIATE_CHALLENGE_RESPONSE":
            return _BRIDGE.initiate_challenge(request)

        if action == "VERIFY_CHALLENGE_RESPONSE":
            try:
                return _BRIDGE.verify_challenge(
                    challenge_id=request["challenge_id"],
                    response=request["response"],
                    epoch=request["epoch"],
                    generation=request["generation"],
                    height=request["height"],
                )
            except KeyError as exc:
                return {
                    "status": "REJECT",
                    "reason": "MISSING_FIELD",
                    "field": str(exc),
                }

        return {"status": "REJECT", "reason": "UNKNOWN_ACTION"}

    return {"status": "REJECT", "reason": "UNKNOWN_COMMAND"}


if __name__ == "__main__":
    import sys

    request = json.load(sys.stdin)
    response = handle(request)
    print(json.dumps(response, indent=2))
