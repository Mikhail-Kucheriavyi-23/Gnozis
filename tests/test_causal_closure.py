from core import State
from core.evolution import evolutionary_transition


def _generate(state):
    yield State(values={"x": state.x + 1, "relations": state.relations})
    yield State(values={"x": state.x + 2, "relations": state.relations})


def _test(candidate):
    return True


def _run(initial, steps=5):
    transition = evolutionary_transition(_generate, _test)
    state = initial
    for _ in range(steps):
        state = transition(state)
    return state


def test_causal_closure_from_initial_state():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})
    assert _run(initial) == _run(initial)
    assert _run(initial).x == 5


def test_external_unrelated_object_does_not_affect_evolution():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})
    unrelated = {"external": "noise"}
    result_without = _run(initial)
    unrelated["external"] = "changed"
    result_with = _run(initial)
    assert result_without == result_with


def test_initial_state_remains_immutable_after_closed_run():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})
    _run(initial)
    assert initial.x == 0
    assert initial.relations == (("a", "b"),)
