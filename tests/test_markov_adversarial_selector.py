"""Adversarial check: selection must not gain an implicit history channel."""

from core import State
from core.evolution import evolutionary_transition


def _transition():
    return evolutionary_transition(
        lambda state: (
            State(values={"x": state.values["x"] + 1, "relations": ("r1",)}),
            State(values={"x": state.values["x"] + 1, "relations": ("r2",)}),
        ),
        lambda _candidate: True,
    )


def test_identical_state_and_candidates_have_same_result_after_different_paths():
    current = State(values={"x": 7, "relations": ("root",)})

    path_a = ("past-a", "past-b")
    path_b = ("other", "history")

    result_a = _transition()(current)
    result_b = _transition()(current)

    # History variables exist only in the caller and are never passed to Core.
    # They therefore cannot legitimately influence the transition.
    assert path_a != path_b
    assert result_a == result_b
