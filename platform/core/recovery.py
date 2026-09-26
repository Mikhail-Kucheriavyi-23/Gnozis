"""Fail-closed recovery boundary."""

from .persistence import Persistence


def recover(persistence: Persistence, state_id: str, expected_digest: str):
    """Recover only when persisted integrity matches the expected digest."""
    stored = persistence.load(state_id, expected_digest=expected_digest)
    return stored.state
