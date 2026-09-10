from core import State
from core.evolution import evolutionary_transition


def _local_generate(state):
    x = dict(state.x)
    relations = tuple(state.relations)
    # Only node a is updated; b is disconnected from a.
    x["a"] += 1
    yield State(values={"x": x, "relations": relations})


def _accept(_candidate):
    return True


def test_disconnected_node_is_unchanged_by_local_transition():
    initial = State(
        values={
            "x": {"a": 0, "b": 10},
            "relations": (("a", "a"),),
        }
    )
    transition = evolutionary_transition(_local_generate, _accept)
    result = transition(initial)

    assert result.x["a"] == 1
    assert result.x["b"] == initial.x["b"]


def test_local_transition_preserves_unrelated_relations():
    initial = State(
        values={
            "x": {"a": 0, "b": 10},
            "relations": (("a", "a"), ("b", "b")),
        }
    )
    transition = evolutionary_transition(_local_generate, _accept)
    result = transition(initial)

    assert result.relations == initial.relations
