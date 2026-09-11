"""Contract test for closure of accepted transitions in the State space."""

from core import State
from core.evolution import evolutionary_transition


def _is_valid_state(state: State) -> bool:
    values = state.values
    return isinstance(values["x"], tuple) and isinstance(values["relations"], tuple)


def test_accepted_candidate_remains_inside_state_space():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    candidate = State(values={"x": ("a", "b"), "relations": (("b", "c"),)})

    result = evolutionary_transition(
        lambda _state: (candidate,),
        _is_valid_state,
    )(initial)

    assert _is_valid_state(result)
    assert result == candidate


def test_invalid_candidate_is_not_repaired_into_state_space():
    initial = State(values={"x": ("a",), "relations": ()})
    invalid = State(values={"x": ["a", "b"], "relations": ()})

    result = evolutionary_transition(
        lambda _state: (invalid,),
        _is_valid_state,
    )

    # No accepted candidate exists; the transition must not silently normalize
    # the invalid candidate into a valid State.
    try:
        result(initial)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid candidate must not be repaired or selected")
