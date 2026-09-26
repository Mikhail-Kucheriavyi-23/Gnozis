"""Trusted persistence boundary."""
from dataclasses import dataclass
from .model import State
from .digest import state_digest

@dataclass(frozen=True)
class StoredState:
    state: State
    digest: str

class Persistence:
    def __init__(self) -> None:
        self._states: dict[str, StoredState] = {}

    def save(self, state: State, digest: str | None = None) -> StoredState:
        computed = state_digest(state)
        if digest is not None and digest != computed:
            raise ValueError("state digest does not match state")
        stored = StoredState(state, computed)
        self._states[state.state_id] = stored
        return stored

    def load(self, state_id: str, expected_digest: str | None = None) -> StoredState:
        stored = self._states[state_id]
        if state_digest(stored.state) != stored.digest:
            raise ValueError("persisted state integrity check failed")
        if expected_digest is not None and stored.digest != expected_digest:
            raise ValueError("state integrity check failed")
        return stored
