from __future__ import annotations

from typing import Callable

from core import Engine, State

from .agency_context import AgencyContext


ContextualTransition = Callable[[State, AgencyContext], State]


def engine_from_agency_context(
    context: AgencyContext,
    transition: ContextualTransition,
) -> Engine:
    """Create a deterministic core Engine from one verified agency context.

    The context is captured at the bridge/core boundary. After construction,
    Engine.step() requires only State, so subsequent evolution is endogenous
    and does not need another authentication or external identity lookup.
    """
    if not context.identity.authenticated:
        raise ValueError("Agency identity is not authenticated")

    def bound_transition(state: State) -> State:
        return transition(state, context)

    return Engine(transition=bound_transition)
