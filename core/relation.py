from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Relation:
    """Immutable relation between two states or system entities."""

    source: Any
    target: Any
    kind: str = "relation"
