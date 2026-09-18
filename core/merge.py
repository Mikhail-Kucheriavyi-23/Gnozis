"""Candidate-level merge and conflict representation.

Merge never directly mutates semantic state. It produces a candidate outcome
which must enter the normal proof/admission/commit pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .state import Psi

T = TypeVar("T")


@dataclass(frozen=True)
class Conflict:
    """A retained incompatibility between two Psi branches."""

    left: Psi
    right: Psi
    reason: str


@dataclass(frozen=True)
class MergeCandidate(Generic[T]):
    """Result of attempting to combine two branches."""

    candidate: T | None
    conflicts: tuple[Conflict, ...] = ()

    @property
    def compatible(self) -> bool:
        return not self.conflicts


def merge(a: Psi, b: Psi) -> MergeCandidate[Psi]:
    """Perform only structurally unambiguous merge.

    Equal X/R is trivially mergeable. Other differences are retained as an
    explicit conflict rather than silently selecting one branch.
    """
    if a == b:
        return MergeCandidate(candidate=a)

    return MergeCandidate(
        candidate=None,
        conflicts=(Conflict(left=a, right=b, reason="non-identical Psi branches"),),
    )
