"""Formal contract for the minimal Psi state transition.

The transition is required to be extensional over the exposed (X, R)
projection: hidden closure state or unrelated State metadata must not affect
its result.
"""

from collections.abc import Callable, Mapping
from typing import Any


PsiProjection = tuple[Any, Any]


def psi_projection(state: Any) -> PsiProjection:
    values = state.values
    return values.get("x"), values.get("relations")


def assert_extensional_transition(
    transition: Callable[[Any], Any],
    make_state: Callable[[Any, Any, Mapping[str, Any]], Any],
    x: Any,
    relations: Any,
) -> None:
    """Require transition output to depend only on (X, R).

    Two states with identical (X, R), but different auxiliary metadata, are
    observationally indistinguishable to the transition contract.
    """
    a = make_state(x, relations, {"hidden": 0})
    b = make_state(x, relations, {"hidden": 10**12})
    ra = transition(a)
    rb = transition(b)
    assert psi_projection(ra) == psi_projection(rb)
