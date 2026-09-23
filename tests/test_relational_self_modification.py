from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_generation_rule_can_evolve_with_relation_state():
    initial = State(
        values={
            "relations": ("a->b",),
            "relation_rule": "append:b->c",
        }
    )

    def generator(state):
        rule = state.values["relation_rule"]
        _, edge = rule.split(":", 1)
        next_rule = "append:c->d" if edge == "b->c" else "append:d->e"
        relations = state.values["relations"] + (edge,)
        return (
            state.evolve(
                values={"relations": relations, "relation_rule": next_rule}
            ),
        )

    def tester(state):
        relations = state.values["relations"]
        return len(relations) >= 2 and state.values["relation_rule"].startswith("append:")

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)
    engine = Engine(transition)

    first = engine.step(initial)
    second = engine.step(first)

    assert first.values["relations"] == ("a->b", "b->c")
    assert first.values["relation_rule"] == "append:c->d"
    assert second.values["relations"] == ("a->b", "b->c", "c->d")
    assert second.values["relation_rule"] == "append:d->e"
    assert first.values["relation_rule"] != second.values["relation_rule"]
