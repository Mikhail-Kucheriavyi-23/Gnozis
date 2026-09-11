"""Adversarial characterization of history independence for identical current State."""

from core import State
from core.evolution import evolutionary_transition


def _next(state, history_marker):
    candidates = (
        State(values={"x": state.values["x"] + 1, "relations": (("a", history_marker),)}),
    )
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(state)


def test_identical_current_state_has_identical_next_state_without_history_input():
    current = State(values={"x": 10, "relations": (("root", "current"),)})

    from_path_a = _next(current, "ignored-history-a")
    from_path_b = _next(current, "ignored-history-b")

    # The transition receives only the current State. Therefore its result
    # must not depend on an unavailable external history channel.
    assert from_path_a == from_path_b


def test_history_is_not_an_implicit_second_state_source():
    current = State(values={"x": 5, "relations": ()})
    before = current.values

    result = evolutionary_transition(
        lambda state: (State(values={"x": state.values["x"] + 1, "relations": ()}),),
        lambda _candidate: True,
    )(current)

    assert current.values == before
    assert result.values["x"] == 6
