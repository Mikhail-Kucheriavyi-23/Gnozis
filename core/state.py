from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .relation import Relation


def _freeze(value: Any) -> Any:
    """Recursively freeze common mutable containers at the State boundary."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, tuple):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class State:
    """Immutable Ψ state: values together with explicit relations."""

    values: Mapping[str, Any] = field(default_factory=dict)
    relations: tuple[Relation, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "values",
            MappingProxyType({k: _freeze(v) for k, v in self.values.items()}),
        )
        object.__setattr__(self, "relations", tuple(self.relations))

    def evolve(
        self,
        *,
        values: Mapping[str, Any],
        relations: tuple[Relation, ...] | None = None,
    ) -> "State":
        """Create a new immutable state while preserving relations by default."""
        return State(
            values=values,
            relations=self.relations if relations is None else relations,
        )
