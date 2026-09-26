"""Immutable Core state and transition model."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class State:
    state_id: str
    version: int
    value: Any


@dataclass(frozen=True)
class Transition:
    transition_id: str
    source_state_id: str
    candidate: Any
