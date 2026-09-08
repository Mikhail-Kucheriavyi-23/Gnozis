from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from .relation import Relation


def _freeze(value: Any) -> Any:
    """Recursively freeze standard mutable containers used in state values."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class State:
    """Immutable computational state Ψ=(X,R).

    ``values`` is the current implementation representation of X.
    ``relations`` is the current implementation representation of R.
    Both are snapshotted at construction time; standard nested containers
    inside ``values`` are recursively frozen.
    """

    values: Mapping[str, Any] = field(default_factory=dict)
    relations: tuple["Relation", ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        frozen_values = _freeze(dict(self.values))
        if not isinstance(frozen_values, Mapping):
            raise TypeError("values must be a mapping")
        object.__setattr__(self, "values", frozen_values)
        object.__setattr__(self, "relations", tuple(self.relations))

    def evolve(
        self,
        *,
        values: Mapping[str, Any] | None = None,
        relations: tuple["Relation", ...] | None = None,
    ) -> "State":
        """Create a new state while preserving unspecified components."""
        return State(
            values=self.values if values is None else values,
            relations=self.relations if relations is None else relations,
        )
