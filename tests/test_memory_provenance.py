from core import State


def memory_from_trajectory(trajectory):
    """Deterministic derived memory: a trace of immutable state projections."""
    return tuple((state.x, state.relations) for state in trajectory)


def test_memory_is_derived_from_trajectory():
    trajectory = [
        State(values={"x": 0, "relations": (("a", "b"),)}),
        State(values={"x": 1, "relations": (("a", "b"),)}),
        State(values={"x": 2, "relations": (("a", "b"),)}),
    ]
    memory = memory_from_trajectory(trajectory)
    assert memory == tuple((s.x, s.relations) for s in trajectory)


def test_same_trajectory_produces_same_memory():
    a = [State(values={"x": 0, "relations": ()}), State(values={"x": 1, "relations": ()})]
    b = [State(values={"x": 0, "relations": ()}), State(values={"x": 1, "relations": ()})]
    assert memory_from_trajectory(a) == memory_from_trajectory(b)


def test_memory_construction_does_not_mutate_history():
    trajectory = [State(values={"x": 0, "relations": (("a", "b"),)})]
    snapshot = list(trajectory)
    memory_from_trajectory(trajectory)
    assert trajectory == snapshot
