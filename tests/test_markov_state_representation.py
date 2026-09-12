"""Adversarial characterization of history independence for identical current State.

The generic State -> State API accepts arbitrary Python callables. Such callables
can close over external data; that is a compatibility-boundary limitation, not
an implicit history channel owned by the canonical Ψ transition.
"""

from core import State
from core.evolution import evolutionary_transition


def _next(state, history_marker):
    candidates = (
        State(values={"x": state.values["x"] + 1, "relations": (("a", history_marker),)}),
    )
    return evolutionary_transition(lambda _s: candidates, lambda _c: True)(state)


def test_legacy_callable_can_close_over_external_data():
    current = State(values={"x": 10, "relations": (("root", "current"),)})

    from_path_a = _next(current, "external-a")
    from_path_b = _next(current, "external-b")

    # This demonstrates the known limitation of the generic callable API:
    # the callable can capture data that is not represented by State.
    assert from_path_a != from_path_b


def test_canonical_transition_has_no_implicit_history_input():
    current = State(values={"x": 5, "relations": ()})
    before = current.values

    result = evolutionary_transition(
        lambda state: (State(values={"x": state.values["x"] + 1, "relations": ()}),),
        lambda _candidate: True,
    )(current)

    assert current.values == before
    assert result.values["x"] == 6


def test_repeated_canonical_transition_from_same_state_is_deterministic():
    current = State(values={"x": 5, "relations": ()})

    generate = lambda state: (
        State(values={"x": state.values["x"] + 1, "relations": ()}),
    )
    transition = evolutionary_transition(generate, lambda _candidate: True)

    assert transition(current) == transition(current)
