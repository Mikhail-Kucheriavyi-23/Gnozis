"""Closure and fixed-point obligations for admissible Psi dynamics."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from .psi_transition import PsiTransition
from .state import Psi

Invariant = Callable[[Psi], bool]


@dataclass(frozen=True)
class ClosureObligation:
    transition: PsiTransition
    invariant: Invariant
    witnesses: tuple[Psi, ...]

    def holds(self) -> bool:
        return all(
            self.invariant(psi) and self.invariant(self.transition(psi))
            for psi in self.witnesses
        )


@dataclass(frozen=True)
class FixedPointObligation:
    transition: PsiTransition
    witnesses: tuple[Psi, ...]

    def holds(self) -> bool:
        return all(self.transition(psi) == psi for psi in self.witnesses)


def closure(
    transition: PsiTransition,
    invariant: Invariant,
    witnesses: Iterable[Psi],
) -> ClosureObligation:
    return ClosureObligation(transition, invariant, tuple(witnesses))


def fixed_point(
    transition: PsiTransition,
    witnesses: Iterable[Psi],
) -> FixedPointObligation:
    return FixedPointObligation(transition, tuple(witnesses))
