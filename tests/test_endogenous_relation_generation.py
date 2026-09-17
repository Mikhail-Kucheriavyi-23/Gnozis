from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_generator_can_create_new_relation_endogenously():
    initial = State(values={"x": 0, "relations": ("a->b",)})

    def generator(state):
        current = state.values["relations"]
        return (
            state.evolve(values={"x": 1, "relations": current + ("b->c",)}),
            state.evolve(values={"x": 0, "relations": current}),
        )

    def tester(state):
        return "b->c" in state.values["relations"]

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    result = Engine(transition).step(initial)

    assert result.values["relations"] == ("a->b", "b->c")
    assert result.values["relations"] != initial.values["relations"]
    assert result.values["x"] == 1
