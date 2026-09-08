from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


def _freeze_entity(value: Any) -> Any:
    """Freeze common mutable containers at the Relation boundary."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze_entity(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_entity(v) for v in value)
    if isinstance(value, tuple):
        return tuple(_freeze_entity(v) for v in value)
    if isinstance(value, set):
        return frozenset(_freeze_entity(v) for v in value)
    return value


@dataclass(frozen=True)
class Relation:
    """Immutable relation between two entities in GNOSIS/UROBOROS."""

    source: Any
    target: Any
    relation_type: str = "related"

    def __post_init__(self) -> None:
        if not isinstance(self.relation_type, str):
            raise TypeError("relation_type must be a string.")

        if not self.relation_type:
            raise ValueError("relation_type must not be empty.")

        object.__setattr__(self, "source", _freeze_entity(self.source))
        object.__setattr__(self, "target", _freeze_entity(self.target))
