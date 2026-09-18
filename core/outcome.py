"""Explicit admissible outcomes for concurrent Ψ branches."""
from __future__ import annotations

from dataclasses import dataclass

from .branch import Branch, incomparable


@dataclass(frozen=True)
class ParallelOutcome:
    """Retains two incomparable branches without selecting either."""

    left: Branch
    right: Branch

    def __post_init__(self) -> None:
        if not incomparable(self.left, self.right):
            raise ValueError("ParallelOutcome requires incomparable branches.")

    @property
    def branches(self) -> tuple[Branch, Branch]:
        return self.left, self.right


def parallel(a: Branch, b: Branch) -> ParallelOutcome:
    """Represent two concurrent branches as one deferred outcome."""
    return ParallelOutcome(a, b)
