"""Immutable Core state and transition model."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any


def freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(freeze(v) for v in value)
    if isinstance(value, tuple):
        return tuple(freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class State:
    state_id: str
    version: int
    value: Any

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", freeze(self.value))


@dataclass(frozen=True)
class Transition:
    transition_id: str
    source_state_id: str
    candidate: Any

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate", freeze(self.candidate))
