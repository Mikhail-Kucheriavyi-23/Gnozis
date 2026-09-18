"""Explicit branch identity and ancestry for concurrent Ψ evolution."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from .state import Psi


@dataclass(frozen=True)
class Branch:
    psi: Psi
    parent: Optional["Branch"] = None
    branch_id: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.psi, Psi):
            raise TypeError("Branch.psi must be Psi.")
        if not self.branch_id:
            object.__setattr__(self, "branch_id", uuid4().hex)

    @property
    def depth(self) -> int:
        return 0 if self.parent is None else self.parent.depth + 1

    def is_ancestor_of(self, other: "Branch") -> bool:
        current = other.parent
        while current is not None:
            if current.branch_id == self.branch_id:
                return True
            current = current.parent
        return False


def incomparable(a: Branch, b: Branch) -> bool:
    """True when neither branch is an ancestor of the other."""
    return not a.is_ancestor_of(b) and not b.is_ancestor_of(a)
