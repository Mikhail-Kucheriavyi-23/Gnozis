from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _hashable(value: Any) -> Any:
    """Return a hashable structural representation without changing State storage."""
    if isinstance(value, Mapping):
        return frozenset((_hashable(k), _hashable(v)) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return tuple(_hashable(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_hashable(v) for v in value)
    hash(value)
    return value


def _freeze(value: Any) -> Any:
    """Recursively freeze the built-in container types used by State."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, tuple):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(_freeze(v) for v in value)
    if isinstance(value, frozenset):
        return frozenset(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class Psi:
    """Fundamental state: exactly the pair Psi=(X,R)."""

    x: Any
    relations: Any


@dataclass(frozen=True)
class State:
    """Extended state with recursively immutable built-in containers."""

    values: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", _freeze(self.values))

    @property
    def x(self) -> Any:
        """Read-only compatibility projection of canonical values['x']."""
        if "x" not in self.values:
            raise AttributeError("State has no canonical 'x' value")
        return self.values["x"]

    @property
    def relations(self) -> Any:
        """Read-only compatibility projection of canonical values['relations']."""
        if "relations" not in self.values:
            raise AttributeError("State has no canonical 'relations' value")
        return self.values["relations"]

    def __hash__(self) -> int:
        """Hash immutable State structurally, without hashing mappingproxy directly."""
        return hash(_hashable(self.values))

    def evolve(self, *, values: Mapping[str, Any]) -> "State":
        """Create a new state without modifying the current state."""
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
