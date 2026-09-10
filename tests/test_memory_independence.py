from core import State
from core.evolution import evolutionary_transition


def _generate(state):
    yield State(values={"x": state.x + 1, "relations": state.relations})


def _test(candidate):
    return True


def _run(state):
    return evolutionary_transition(_generate, _test)(state)


def test_memory_representation_is_not_an_implicit_state_channel():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})
    memory_a = ((0, initial.relations),)
    memory_b = ((999, (("unrelated", "edge"),)),)
    assert _run(initial) == _run(initial)
    assert memory_a != memory_b


def test_evolution_depends_on_declared_state_not_external_memory():
    initial = State(values={"x": 4, "relations": ()})
    external_memory = {"history": ["noise"]}
    result_a = _run(initial)
    external_memory["history"].append("changed")
    result_b = _run(initial)
    assert result_a == result_b


def test_memory_must_be_explicit_if_it_is_to_affect_evolution():
    initial = State(values={"x": 0, "relations": ()})
    baseline = _run(initial)
    hidden_memory = {"preferred_x": 1000}
    assert _run(initial) == baseline
    assert hidden_memory["preferred_x"] == 1000
