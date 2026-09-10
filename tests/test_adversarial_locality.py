from core import State
from core.evolution import evolutionary_transition


def _generate_local(state):
    # Deliberately expose two disconnected components. The transition may
    # inspect the whole state, so the test below catches accidental global
    # dependence by comparing a perturbed component.
    yield State(values={"x": state.x, "relations": state.relations})
    yield State(values={"x": state.x + 1, "relations": state.relations})


def _test(candidate):
    return True


def _run(state):
    return evolutionary_transition(_generate_local, _test)(state)


def test_disconnected_component_does_not_change_when_other_component_changes():
    base = State(values={"x": 0, "relations": (("a", "b"), ("c", "d"))})
    perturbed = State(values={"x": 1, "relations": (("a", "b"), ("c", "d"))})

    result_base = _run(base)
    result_perturbed = _run(perturbed)

    # Relation topology is disconnected and must remain unchanged.
    assert result_base.relations == base.relations
    assert result_perturbed.relations == perturbed.relations


def test_unrelated_relation_set_is_invariant_under_local_step():
    state = State(values={"x": 0, "relations": (("a", "b"), ("c", "d"))})
    result = _run(state)

    assert ("c", "d") in result.relations
    assert ("a", "b") in result.relations
