from core import State
from core.evolution import evolutionary_transition


def _generate(state):
    # Two deterministic candidates derived only from the current state.
    yield State(values={"x": state.x + 1, "relations": state.relations})
    yield State(values={"x": state.x + 2, "relations": state.relations})


def _test(candidate):
    return True


def _run(initial, steps=5):
    transition = evolutionary_transition(_generate, _test)
    state = initial
    trajectory = [state]
    for _ in range(steps):
        state = transition(state)
        trajectory.append(state)
    return trajectory


def test_closed_evolution_is_reproducible_from_same_initial_state():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})

    first = _run(initial)
    second = _run(initial)

    assert first == second
    assert first[0] == initial
    assert first[-1].x == 5


def test_evolution_does_not_mutate_initial_state():
    initial = State(values={"x": 0, "relations": (("a", "b"),)})
    _run(initial)

    assert initial.x == 0
    assert initial.relations == (("a", "b"),)
