"""Proof-carrying meta-transitions for protected self-evolution."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .root_invariant import RootInvariant, preserve_root

T = TypeVar("T")


@dataclass(frozen=True)
class RefinementProof(Generic[T]):
    """Evidence that a proposed meta-transition preserves K0."""

    root: RootInvariant[T]
    before: T
    after: T
    statement: str

    @property
    def valid(self) -> bool:
        return bool(self.statement.strip()) and preserve_root(
            self.root, self.before, self.after
        )


@dataclass(frozen=True)
class MetaTransition(Generic[T]):
    """A proposed kernel/meta-state change carrying a refinement proof."""

    before: T
    after: T
    proof: RefinementProof[T]

    def admissible(self) -> bool:
        return (
            self.proof.before == self.before
            and self.proof.after == self.after
            and self.proof.valid
        )

    def apply(self) -> T:
        if not self.admissible():
            raise ValueError("meta-transition is not admitted by its refinement proof")
        return self.after
