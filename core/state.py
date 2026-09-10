from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .relation import Relation


class _FrozenSequence(tuple):
    """Immutable sequence retaining list-compatible equality for API compatibility."""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, list):
            return tuple(self) == tuple(other)
        return super().__eq__(other)


def _freeze(value: Any) -> Any:
    """Recursively freeze the built-in container types used by State."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return _FrozenSequence(_freeze(v) for v in value)
    if isinstance(value, tuple):
        return _FrozenSequence(_freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(_freeze(v) for v in value)
    if isinstance(value, frozenset):
        return frozenset(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class Psi:
    """Fundamental immutable state Ψ=(X,R)."""

    x: Any
    relations: tuple[Relation, ...]

    def __post_init__(self) -> None:
        relations = tuple(self.relations)
        if any(not isinstance(relation, Relation) for relation in relations):
            raise TypeError("Psi.relations must contain only Relation instances")
        object.__setattr__(self, "relations", relations)


@dataclass(frozen=True)
class State:
    """Compatibility/application wrapper around the fundamental Psi state."""

    values: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", _freeze(self.values))

    def __getattr__(self, name: str) -> Any:
        """Expose legacy field-style access without creating a second state model."""
        values = object.__getattribute__(self, "values")
        try:
            return values[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def evolve(self, *, values: Mapping[str, Any]) -> "State":
        """Create a new state without modifying the current state."""
        return State(values=values)

    def to_psi(self) -> Psi:
        """Project the wrapper onto its explicit fundamental Ψ=(X,R) state."""
        if "x" not in self.values or "relations" not in self.values:
            raise ValueError("State must contain fundamental fields 'x' and 'relations'")
        return Psi(self.values["x"], tuple(self.values["relations"]))

    @classmethod
    def from_psi(cls, psi: Psi) -> "State":
        """Adapt a fundamental Psi state into the application wrapper."""
        if not isinstance(psi, Psi):
            raise TypeError("psi must be a Psi instance")
        return cls(values={"x": psi.x, "relations": psi.relations})
