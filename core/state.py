from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .relation import Relation


@dataclass(frozen=True)
class State:
    """Immutable Ψ state: values together with explicit relations."""

    values: Mapping[str, Any] = field(default_factory=dict)
    relations: tuple[Relation, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", dict(self.values))
        object.__setattr__(self, "relations", tuple(self.relations))

    def evolve(
        self,
        *,
        values: Mapping[str, Any],
        relations: tuple[Relation, ...] | None = None,
    ) -> "State":
        """Create a new immutable state while preserving relations by default."""
        return State(
            values=dict(values),
            relations=self.relations if relations is None else tuple(relations),
        )
