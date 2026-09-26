"""Minimal persistence boundary for trusted Core state."""

from dataclasses import dataclass
from .model import State


@dataclass(frozen=True)
class StoredState:
    state: State
    digest: str


class Persistence:
    def __init__(self) -> None:
        self._states: dict[str, StoredState] = {}

    def save(self, state: State, digest: str) -> StoredState:
        if not digest:
            raise ValueError("state digest is required")
        stored = StoredState(state=state, digest=digest)
        self._states[state.state_id] = stored
        return stored

    def load(self, state_id: str, expected_digest: str | None = None) -> StoredState:
        try:
            stored = self._states[state_id]
        except KeyError as exc:
            raise KeyError("state not found") from exc
        if expected_digest is not None and stored.digest != expected_digest:
            raise ValueError("state integrity check failed")
        return stored
