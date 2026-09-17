from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_relations_survive_generate_test_select():
    initial = State(values={"x": 0, "relations": ("a->b",)})

    candidate_a = initial.evolve(values={"x": 1, "relations": ("a->b",)})
    candidate_b = initial.evolve(values={"x": 0, "relations": ("a->c",)})

    def generator(state):
        return (candidate_a, candidate_b)

    def tester(state):
        return state.values["relations"] == ("a->b",)

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    result = Engine(transition).step(initial)

    assert result.values["relations"] == ("a->b",)
    assert result.values["x"] == 1


def test_empty_relations_preserve_existing_evolution_behavior():
    initial = State(values={"x": 0, "relations": ()})

    def generator(state):
        return (state.evolve(values={"x": 1, "relations": ()}),)

    def tester(state):
        return state.values["x"] == 1

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    result = Engine(transition).step(initial)

    assert result.values["x"] == 1
    assert result.values["relations"] == ()
