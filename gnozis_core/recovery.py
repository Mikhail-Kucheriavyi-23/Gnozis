"""Fail-closed recovery boundary."""
from .persistence import Persistence

def recover(persistence: Persistence, state_id: str, expected_digest: str):
    return persistence.load(state_id, expected_digest=expected_digest).state
