from core.engine import Engine
from core.evolution import evolutionary_transition
from core.state import State


def test_adversarial_relations_select_only_valid_candidate():
    initial = State(values={"x": 0, "relations": ("a->b",)})

    valid = initial.evolve(values={"x": 1, "relations": ("a->b", "b->c")})
    invalid = initial.evolve(values={"x": 99, "relations": ("a->b", "conflict")})

    def generator(state):
        return (invalid, valid)

    def tester(state):
        relations = state.values["relations"]
        return "conflict" not in relations and all("->" in r for r in relations)

    def selector(candidates):
        return max(candidates, key=lambda state: state.values["x"])

    transition = evolutionary_transition(generator, tester, selector)
    result = Engine(transition).step(initial)

    assert result.values["relations"] == ("a->b", "b->c")
    assert result.values["x"] == 1


def test_adversarial_conflict_does_not_escape_when_all_candidates_invalid():
    initial = State(values={"x": 0, "relations": ("a->b",)})
    bad_a = initial.evolve(values={"x": 10, "relations": ("a->b", "conflict")})
    bad_b = initial.evolve(values={"x": 20, "relations": ("a->b", "broken")})

    def generator(state):
        return (bad_a, bad_b)

    def tester(state):
        return all("->" in r for r in state.values["relations"])

    def selector(candidates):
        return candidates[0]

    transition = evolutionary_transition(generator, tester, selector)

    try:
        Engine(transition).step(initial)
    except (ValueError, RuntimeError):
        return

    raise AssertionError("invalid relational candidates escaped Test/Select")
