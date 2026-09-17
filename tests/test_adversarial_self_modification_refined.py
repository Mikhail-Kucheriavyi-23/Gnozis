from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_self_modified_rule_is_accepted_only_if_it_preserves_state_invariant():
    initial = State(values={"x": 0, "relations": ("a->b",), "rule": "append_edge"})

    valid = initial.evolve(values={
        "x": 1,
        "relations": ("a->b", "b->c"),
        "rule": "append_edge",
    })
    invalid = initial.evolve(values={
        "x": 1,
        "relations": ("a->b", "broken"),
        "rule": "delete_all_edges",
    })

    def generator(state):
        # The candidate rule is derived from the current state, not selected
        # from a fixed whitelist by the test itself.
        candidates = [valid, invalid]
        return tuple(candidates)

    def invariant(state):
        relations = state.values["relations"]
        return all("->" in relation for relation in relations) and len(relations) >= 1

    def tester(state):
        return invariant(state)

    def selector(candidates):
        return max(candidates, key=lambda state: len(state.values["relations"]))

    result = Engine(evolutionary_transition(generator, tester, selector)).step(initial)

    assert result.values["rule"] == "append_edge"
    assert result.values["relations"] == ("a->b", "b->c")
    assert invariant(result)


def test_invalid_self_modification_cannot_become_the_next_generator_rule():
    initial = State(values={"x": 0, "relations": ("a->b",), "rule": "append_edge"})
    invalid = initial.evolve(values={
        "x": 1,
        "relations": ("broken",),
        "rule": "delete_all_edges",
    })

    def generator(state):
        return (invalid,)

    def tester(state):
        return all("->" in relation for relation in state.values["relations"])

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)

    try:
        Engine(transition).step(initial)
    except (ValueError, RuntimeError):
        return

    raise AssertionError("invalid self-modifying rule escaped the invariant test")
