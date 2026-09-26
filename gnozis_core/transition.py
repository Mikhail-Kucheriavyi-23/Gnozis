from .model import State, Transition


def validate_transition(source: State, transition: Transition) -> None:
    if transition.source_state_id != source.state_id:
        raise ValueError("transition source does not match current state")
    if not transition.transition_id:
        raise ValueError("transition_id is required")
