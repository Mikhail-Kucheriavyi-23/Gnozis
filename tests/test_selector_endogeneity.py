"""Adversarial checks that selection depends only on candidate states."""

from core import State
from core.evolution import evolutionary_transition


def _run(candidates, external):
    # The external value is deliberately present in the caller but is not part
    # of any candidate and must not affect endogenous selection.
    _ = external
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(
        State(values={"x": 0, "relations": ()})
    )


def test_selection_is_independent_of_unrelated_external_context():
    candidates = (
        State(values={"x": 1, "relations": (("z", "q"),)}),
        State(values={"x": 1, "relations": (("a", "b"),)}),
    )

    first = _run(candidates, {"noise": 1})
    second = _run(candidates, {"noise": 999, "clock": 123456})

    assert first == second


def test_selection_is_reproducible_for_identical_candidate_states():
    candidate = State(values={"x": 1, "relations": (("a", "b"),)})
    candidates = (candidate,)

    first = _run(candidates, object())
    second = _run(candidates, object())

    assert first == second
