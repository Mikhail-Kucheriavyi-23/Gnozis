from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Relation:
    """Immutable relation between two entities in GNOSIS/UROBOROS."""

    source: Any
    target: Any
    relation_type: str

    def __post_init__(self) -> None:
        if not isinstance(self.relation_type, str):
            raise TypeError("relation_type must be a string.")

        if not self.relation_type:
            raise ValueError("relation_type must not be empty.")

