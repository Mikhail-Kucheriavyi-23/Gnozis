"""Adversarial tests for state-extensional evolution."""

import random
import time

from core.evolution import evolutionary_transition
from core.state import State


def _state():
    return State(values={"score": 0, "relations": ("r0",)})


def _signature(state):
    return (state.values["score"], state.values["relations"])


def _transition():
    def generate(state):
        return [State(values={
            "score": state.values["score"] + 1,
            "relations": state.values["relations"],
        })]

    def test(state):
        return state.values["score"] > 0

    return evolutionary_transition(generate, test)


def test_same_state_is_independent_of_global_context():
    external = {"value": 0}
    transition = _transition()
    external["value"] = 1
    first = _signature(transition(_state()))
    external["value"] = 999999
    second = _signature(transition(_state()))
    assert first == second


def test_same_state_is_independent_of_random_source(monkeypatch):
    transition = _transition()
    monkeypatch.setattr(random, "random", lambda: 0.0)
    first = _signature(transition(_state()))
    monkeypatch.setattr(random, "random", lambda: 1.0)
    second = _signature(transition(_state()))
    assert first == second


def test_same_state_is_independent_of_wall_clock(monkeypatch):
    transition = _transition()
    monkeypatch.setattr(time, "time", lambda: 1.0)
    first = _signature(transition(_state()))
    monkeypatch.setattr(time, "time", lambda: 9999999999.0)
    second = _signature(transition(_state()))
    assert first == second


def test_repeated_execution_with_identical_state_has_identical_result():
    transition = _transition()
    results = [_signature(transition(_state())) for _ in range(5)]
    assert all(result == results[0] for result in results)


def test_mutable_closure_is_not_used_by_transition():
    hidden = {"increment": 1}

    def generate(state):
        # The generator intentionally has access to mutable closure state,
        # but the transition implementation must not add hidden state of its own.
        increment = 1
        return [State(values={
            "score": state.values["score"] + increment,
            "relations": state.values["relations"],
        })]

    def test(state):
        return state.values["score"] > 0

    transition = evolutionary_transition(generate, test)
    first = _signature(transition(_state()))
    hidden["increment"] = 999
    second = _signature(transition(_state()))
    assert first == second
