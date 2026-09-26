"""Minimal verification boundary."""

from .model import State, Transition


def verify_transition(source: State, transition: Transition, accepted: bool) -> bool:
    """Return acceptance only after structural validation."""
    if not accepted:
        return False
    if transition.source_state_id != source.state_id:
        return False
    return True
