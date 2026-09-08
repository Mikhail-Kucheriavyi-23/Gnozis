"""Boundary for the fundamental Psi transition.

The fundamental operator is intentionally defined on the exposed pair (X, R),
not on the richer State object. This makes hidden State fields inaccessible by
construction at the API boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Hashable, Iterable, Tuple

X = Any
R = Any
PsiResult = Tuple[X, R]
PureTransition = Callable[[X, R], PsiResult]


@dataclass(frozen=True)
class PsiTransition:
    """Explicit fundamental transition F(X, R) -> (X', R')."""

    function: PureTransition

    def __call__(self, x: X, relations: R) -> PsiResult:
        result = self.function(x, relations)
        if not isinstance(result, tuple) or len(result) != 2:
            raise TypeError("Psi transition must return exactly (X', R')")
        return result


def apply_transition(
    transition: PsiTransition,
    x: X,
    relations: R,
) -> PsiResult:
    """Apply the fundamental transition using only X and R."""
    return transition(x, relations)
