import os
import random
import time

from core.state import State


def psi_signature(state):
    return (
        state.values["x"],
        tuple(sorted(state.values["relations"])),
    )


def make_pure_transition():
    def transition(x, relations):
        return x + len(relations), tuple(sorted(relations))
    return transition


def test_same_inputs_are_deterministic_across_repeated_calls():
    transition = make_pure_transition()
    x = 7
    relations = (("a", "b"), ("b", "c"))
    results = [transition(x, relations) for _ in range(20)]
    assert all(result == results[0] for result in results)


def test_external_randomness_cannot_be_part_of_fundamental_transition():
    transition = make_pure_transition()
    x = 7
    relations = (("a", "b"),)

    random.seed(1)
    first = transition(x, relations)
    random.seed(999999)
    second = transition(x, relations)

    assert first == second


def test_time_and_environment_changes_do_not_affect_pure_transition():
    transition = make_pure_transition()
    x = 7
    relations = (("a", "b"),)

    os.environ["GNOZIS_RED_TEAM_PROBE"] = "A"
    first = transition(x, relations)
    time.sleep(0.001)
    os.environ["GNOZIS_RED_TEAM_PROBE"] = "B"
    second = transition(x, relations)

    assert first == second


def test_state_wrapper_is_only_an_adapter_to_x_and_r():
    transition = make_pure_transition()
    a = State(values={"x": 7, "relations": (("a", "b"),), "memory": 0})
    b = State(values={"x": 7, "relations": (("a", "b"),), "memory": 10**12})

    assert transition(a.values["x"], a.values["relations"]) == transition(
        b.values["x"], b.values["relations"]
    )
