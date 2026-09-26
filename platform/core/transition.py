"""Minimal trusted transition validation."""

from .model import State, Transition


def validate_transition(source: State, transition: Transition) -> None:
    """Fail closed when a transition does not match its declared source."""
    if transition.source_state_id != source.state_id:
        raise ValueError("transition source does not match current state")
    if not transition.transition_id:
        raise ValueError("transition_id is required")
