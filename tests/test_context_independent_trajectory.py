"""Adversarial checks for trajectory independence from unrelated external context."""

from core import State
from core.evolution import evolutionary_transition


def _run(initial, external_context):
    candidates = (
        State(values={"x": 1, "relations": (("a", "b"),)}),
        State(values={"x": 1, "relations": (("c", "d"),)}),
    )

    def test(candidate):
        # The external object is deliberately available but must not influence
        # acceptance or selection.
        _ = external_context
        return True

    return evolutionary_transition(lambda _s: candidates, test)(initial)


def test_same_initial_state_is_independent_of_unrelated_external_context():
    initial = State(values={"x": 0, "relations": ()})

    first = _run(initial, {"noise": 1})
    second = _run(initial, {"noise": 999, "other": ["changed"]})

    assert first == second


def test_same_candidates_are_reproducible_when_external_context_changes():
    initial = State(values={"x": 0, "relations": ()})
    contexts = [None, {"clock": 123}, {"random": 0.731}, object()]

    results = [_run(initial, context) for context in contexts]

    assert all(result == results[0] for result in results)
