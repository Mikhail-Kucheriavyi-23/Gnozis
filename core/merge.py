"""Candidate-level merge and conflict representation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .branch import Branch
from .state import Psi

T = TypeVar("T")


@dataclass(frozen=True)
class Conflict:
    """A retained incompatibility between two branches."""

    left: Branch
    right: Branch
    reason: str

    @property
    def source_psis(self) -> tuple[Psi, Psi]:
        return self.left.psi, self.right.psi


@dataclass(frozen=True)
class MergeCandidate(Generic[T]):
    candidate: T | None
    conflicts: tuple[Conflict, ...] = ()

    @property
    def compatible(self) -> bool:
        return not self.conflicts


def merge(a: Branch, b: Branch) -> MergeCandidate[Psi]:
    """Merge branches without silently selecting a conflicting branch."""
    if a.psi == b.psi:
        return MergeCandidate(candidate=a.psi)
    return MergeCandidate(
        candidate=None,
        conflicts=(Conflict(left=a, right=b, reason="non-identical Psi branches"),),
    )
