"""Minimal Core state/transition model boundary."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class State:
    """Immutable versioned runtime state."""

    state_id: str
    version: int
    value: Any


@dataclass(frozen=True)
class Transition:
    """An attempted change from one state to another."""

    transition_id: str
    source_state_id: str
    candidate: Any
