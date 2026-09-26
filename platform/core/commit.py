"""Minimal trusted commit boundary."""

from .model import State, Transition
from .transition import validate_transition
from .verify import verify_transition
from .digest import state_digest


def commit(source: State, transition: Transition, accepted: bool) -> State:
    """Create the next immutable state only after validation and acceptance."""
    validate_transition(source, transition)
    if not verify_transition(source, transition, accepted):
        raise ValueError("transition verification failed")
    result = State(state_id=transition.transition_id, version=source.version + 1, value=transition.candidate)
    if not state_digest(result):
        raise ValueError("committed state integrity identity missing")
    return result
