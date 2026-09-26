from core.state import State
from core.evolution import evolutionary_psi_transition


def test_canonical_psi_selector_is_permutation_invariant():
    candidates = (
        State(values={"x": 1, "relations": (("z", "q"),)}),
        State(values={"x": 1, "relations": (("a", "b"),)}),
        State(values={"x": 2, "relations": ()}),
    )

    def generate(_state):
        return candidates

    def test(_candidate):
        return True

    transition = evolutionary_psi_transition(generate, test)
    first = transition.function(0, ())
    second = transition.function(0, ())
    assert first == second


def test_current_psi_selector_does_not_claim_x_monotonicity():
    candidates = (
        State(values={"x": 100, "relations": (("z", "q"),)}),
        State(values={"x": 1, "relations": ()}),
    )

    transition = evolutionary_psi_transition(lambda _s: candidates, lambda _c: True)
    result = transition.function(0, ())

    assert result == State(values={"x": 1, "relations": ()}).to_psi().x, result[0]
