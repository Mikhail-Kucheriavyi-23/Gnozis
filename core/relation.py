from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Relation:
    """Structurally immutable relation record.

    ``source`` and ``target`` are intentionally unconstrained. If either is a
    mutable object, that object's internal state is outside Relation's
    immutability boundary.
    """

    source: Any
    target: Any
    relation_type: str = "related"

    def __post_init__(self) -> None:
        if not isinstance(self.relation_type, str):
            raise TypeError("relation_type must be a string.")

        if not self.relation_type:
            raise ValueError("relation_type must not be empty.")
