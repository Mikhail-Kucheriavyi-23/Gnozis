"""Trusted commit boundary."""
from .model import State, Transition
from .transition import validate_transition
from .verify import verify_transition
from .digest import state_digest


def commit(source: State, transition: Transition, accepted: bool) -> State:
    validate_transition(source, transition)
    if not verify_transition(source, transition, accepted):
        raise ValueError("transition verification failed")
    result = State(transition.transition_id, source.version + 1, transition.candidate)
    state_digest(result)
    return result
