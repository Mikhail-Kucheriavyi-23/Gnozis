"""Adversarial tests for external selector injection and candidate ordering."""

from core import State
from core.evolution import evolutionary_transition, select_next_state


def _candidate(name: str, relations):
    return State(values={"name": name, "relations": tuple(relations)})


def test_external_selector_cannot_override_endogenous_selection():
    initial = State(values={"name": "initial", "relations": ()})
    preferred = _candidate("preferred", (("a", "b"),))
    other = _candidate("other", (("a", "b"), ("b", "c")))

    def generate(_state):
        return (preferred, other)

    def test(_state):
        return True

    # No selector is accepted by the transition contract. An attempted
    # external selector therefore has no control path into selection.
    transition = evolutionary_transition(generate, test)
    result = transition(initial)

    assert result == preferred


def test_candidate_order_does_not_change_selection():
    initial = State(values={"name": "initial", "relations": ()})
    a = _candidate("a", (("x", "y"),))
    b = _candidate("b", (("x", "y"), ("y", "z")))

    def test(_state):
        return True

    result_ab = select_next_state(initial, lambda _s: (a, b), test)
    result_ba = select_next_state(initial, lambda _s: (b, a), test)

    assert result_ab == result_ba == a
