from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_relation_evolves_across_two_generations():
    initial = State(values={"x": 0, "relations": ("a->b",)})

    generation_1 = initial.evolve(
        values={"x": 1, "relations": ("b->c",)}
    )
    generation_2 = generation_1.evolve(
        values={"x": 2, "relations": ("c->d",)}
    )

    def generator_1(state):
        return (generation_1,)

    def tester_1(state):
        return state.values["relations"] == ("b->c",)

    def selector(candidates):
        return candidates[0]

    transition_1 = evolutionary_transition(generator_1, tester_1, selector)
    result_1 = Engine(transition_1).step(initial)

    assert result_1.values["relations"] == ("b->c",)
    assert result_1.values["x"] == 1

    def generator_2(state):
        return (generation_2,)

    def tester_2(state):
        return state.values["relations"] == ("c->d",)

    transition_2 = evolutionary_transition(generator_2, tester_2, selector)
    result_2 = Engine(transition_2).step(result_1)

    assert result_2.values["relations"] == ("c->d",)
    assert result_2.values["x"] == 2
    assert result_1.values["relations"] != result_2.values["relations"]
