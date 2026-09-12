from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_rule_is_generated_from_current_state_and_used_next_generation():
    initial = State(values={"x": 0, "relations": ("a->b",), "rule": "add_b_to_c"})

    def generator(state):
        rule = state.values["rule"]
        relation = state.values["relations"]
        if rule == "add_b_to_c":
            next_state = state.evolve(values={
                "x": state.values["x"] + 1,
                "relations": relation + ("b->c",),
                "rule": "add_c_to_d",
            })
        else:
            next_state = state.evolve(values={
                "x": state.values["x"] + 1,
                "relations": relation + ("c->d",),
                "rule": "halt",
            })
        return (next_state,)

    def tester(state):
        return state.values["rule"] in {"add_c_to_d", "halt"}

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)

    result_1 = Engine(transition).step(initial)
    result_2 = Engine(transition).step(result_1)

    assert result_1.values["rule"] == "add_c_to_d"
    assert result_1.values["relations"] == ("a->b", "b->c")
    assert result_2.values["rule"] == "halt"
    assert result_2.values["relations"] == ("a->b", "b->c", "c->d")
