from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_local_update_is_independent_of_remote_state():
    local_a = State(values={"nodes": {"a": 0, "b": 0}, "relations": (("a", "b"),)})
    local_b = State(values={"nodes": {"a": 0, "b": 100}, "relations": (("a", "b"),)})

    def generator(state):
        nodes = dict(state.values["nodes"])
        # a changes only from its own value and its direct neighbor b.
        nodes["a"] = nodes["a"] + (1 if nodes["b"] > 0 else 0)
        return (state.evolve(values={"nodes": nodes}),)

    def tester(state):
        return True

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    result_a = Engine(transition).step(local_a)
    result_b = Engine(transition).step(local_b)

    assert result_a.values["nodes"]["a"] == 0
    assert result_b.values["nodes"]["a"] == 1


def test_disconnected_remote_component_does_not_affect_local_update():
    state_1 = State(values={"nodes": {"a": 1, "b": 2, "z": 10}, "relations": (("a", "b"),)})
    state_2 = State(values={"nodes": {"a": 1, "b": 2, "z": 9999}, "relations": (("a", "b"),)})

    def generator(state):
        nodes = dict(state.values["nodes"])
        nodes["a"] = nodes["a"] + nodes["b"]
        return (state.evolve(values={"nodes": nodes}),)

    def tester(state):
        return True

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    result_1 = Engine(transition).step(state_1)
    result_2 = Engine(transition).step(state_2)

    assert result_1.values["nodes"]["a"] == result_2.values["nodes"]["a"] == 3
