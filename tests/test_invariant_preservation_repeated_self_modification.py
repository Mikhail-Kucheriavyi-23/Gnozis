from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_invariant_is_preserved_at_every_generation_under_self_modification():
    initial = State(values={"x": 0, "relations": (), "rule": "append"})

    def generator(state):
        n = state.values["x"]
        relation = f"r{n}->r{n + 1}"
        return (state.evolve(values={
            "x": n + 1,
            "relations": state.values["relations"] + (relation,),
            "rule": "append",
        }),)

    def invariant(state):
        relations = state.values["relations"]
        return (
            state.values["x"] == len(relations)
            and all("->" in r for r in relations)
            and state.values["rule"] == "append"
        )

    def tester(state):
        return invariant(state)

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    state = initial

    for generation in range(1, 101):
        state = Engine(transition).step(state)
        assert invariant(state), f"invariant failed at generation {generation}"

    assert state.values["x"] == 100
    assert len(state.values["relations"]) == 100
