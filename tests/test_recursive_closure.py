from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_recursive_self_modification_closes_for_many_generations():
    initial = State(values={"x": 0, "relations": (), "rule": "add_0"})

    def generator(state):
        rule = state.values["rule"]
        x = state.values["x"]
        relations = state.values["relations"]
        n = int(rule.split("_")[1])
        next_n = n + 1
        return (state.evolve(values={
            "x": x + 1,
            "relations": relations + (f"r{n}->r{next_n}",),
            "rule": f"add_{next_n}",
        }),)

    def tester(state):
        return state.values["rule"].startswith("add_")

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    state = initial

    for _ in range(10):
        state = Engine(transition).step(state)

    assert state.values["x"] == 10
    assert state.values["rule"] == "add_10"
    assert len(state.values["relations"]) == 10
    assert state.values["relations"][0] == "r0->r1"
    assert state.values["relations"][-1] == "r9->r10"
