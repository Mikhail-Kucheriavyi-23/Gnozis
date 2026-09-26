"""Formal contracts for the minimal Psi state transition."""

from collections.abc import Callable, Mapping
from typing import Any

from .state import Psi
from .psi_transition import PsiTransition


PsiProjection = tuple[Any, Any]
Projection = Callable[[Any], PsiProjection]


def psi_projection(state: Any) -> PsiProjection:
    """Return the complete fundamental (X, R) projection of a State."""
    values = state.values
    return values.get("x"), values.get("relations")


def assert_extensional_transition(
    transition: Callable[[Any], Any],
    make_state: Callable[[Any, Any, Mapping[str, Any]], Any],
    x: Any,
    relations: Any,
    projection: Projection = psi_projection,
) -> None:
    """Require transition output to be extensional over (X, R).

    Auxiliary metadata may be present in a concrete State, but it is not
    allowed to change the fundamental transition.  Equivalence is defined by
    the supplied Psi projection rather than by incidental implementation
    fields.
    """
    a = make_state(x, relations, {"hidden": 0})
    b = make_state(x, relations, {"hidden": 10**12})
    ra = transition(a)
    rb = transition(b)
    assert projection(ra) == projection(rb), (
        "Psi extensionality violated: identical (X, R) produced different "
        "fundamental transition results"
    )

def assert_extensional_psi_transition(
    transition: PsiTransition,
    psi: Psi,
    mutate_hidden: Callable[[], None],
) -> None:
    """Require one canonical ΨTransition to be extensional over Ψ.

    The same canonical input is evaluated before and after controlled hidden
    state mutation. A difference proves that information outside (X, R)
    influences the fundamental transition.
    """
    if not isinstance(transition, PsiTransition):
        raise TypeError("transition must be a PsiTransition")
    if not isinstance(psi, Psi):
        raise TypeError("psi must be a Psi")

    before = transition(psi)
    mutate_hidden()
    after = transition(psi)

    assert before == after, (
        "Psi extensionality violated: identical canonical Ψ produced "
        "different transition results after hidden-state mutation"
    )


def assert_same_transition_for_same_projection(
    transition: Callable[[Any], Any],
    states: list[Any],
    projection: Projection = psi_projection,
) -> None:
    """Check extensionality across an arbitrary family of states.

    This is stronger than a single hidden-variable example: every state in
    the family must produce the same fundamental result whenever all states
    share the same (X, R) projection.
    """
    if not states:
        return
    reference = projection(transition(states[0]))
    expected_input = projection(states[0])
    for state in states[1:]:
        assert projection(state) == expected_input
        assert projection(transition(state)) == reference, (
            "Psi extensionality violated for a member of the adversarial family"
        )
