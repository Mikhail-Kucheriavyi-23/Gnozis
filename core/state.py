from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _freeze(value: Any) -> Any:
    """Recursively freeze standard mutable containers.

    Arbitrary domain objects are intentionally left untouched: Ψ permits
    arbitrary entities, and imposing a universal object-level immutability
    protocol would change the mathematical domain of X.
    """
    if isinstance(value, Mapping):
        return MappingProxyType(
            {_freeze(key): _freeze(item) for key, item in value.items()}
        )
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class Psi:
    """Fundamental state: exactly the pair Psi=(X,R)."""

    x: Any
    relations: Any


@dataclass(frozen=True)
class State:
    """Extended immutable state; metadata is not fundamental Psi state."""

    values: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", _freeze(self.values))

    def evolve(self, *, values: Mapping[str, Any]) -> "State":
        """Create a new deeply container-immutable state."""
        return State(values=values)

    def to_psi(self) -> Psi:
        """Project extended state onto its fundamental Psi=(X,R) component."""
        if "x" not in self.values or "relations" not in self.values:
            raise ValueError("State must contain fundamental fields 'x' and 'relations'")
        return Psi(self.values["x"], self.values["relations"])

    @classmethod
    def from_psi(cls, psi: Psi) -> "State":
        """Adapt a fundamental Psi state into an extended State."""
        return cls(values={"x": psi.x, "relations": psi.relations})
