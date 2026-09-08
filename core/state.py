from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Psi:
    """Fundamental state: exactly the pair Psi=(X,R)."""

    x: Any
    relations: Any


@dataclass(frozen=True)
class State:
    """Extended immutable state; metadata is not fundamental Psi state."""

    values: Mapping[str, Any] = field(default_factory=dict)

    def evolve(self, *, values: Mapping[str, Any]) -> "State":
        """Create a new state without modifying the current state."""
        return State(values=dict(values))

    def to_psi(self) -> Psi:
        """Project extended state onto its fundamental Psi=(X,R) component."""
        if "x" not in self.values or "relations" not in self.values:
            raise ValueError("State must contain fundamental fields 'x' and 'relations'")
        return Psi(self.values["x"], self.values["relations"])

    @classmethod
    def from_psi(cls, psi: Psi) -> "State":
        """Adapt a fundamental Psi state into an extended State."""
        return cls(values={"x": psi.x, "relations": psi.relations})
