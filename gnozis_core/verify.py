from .model import State, Transition


def verify_transition(source: State, transition: Transition, accepted: bool) -> bool:
    if not accepted:
        return False
    if transition.source_state_id != source.state_id:
        return False
    return True
