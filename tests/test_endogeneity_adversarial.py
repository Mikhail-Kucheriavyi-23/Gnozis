"""Adversarial tests for state-extensional evolution.

These tests are deliberately black-box: the same canonical State must not
produce different evolution outcomes merely because hidden process context
(global state, mutable closure state, randomness, or wall-clock time) changes.
"""

import random
import time

from core.evolution import EndogenousEvolution
from core.state import State


def _state(values=None):
    return State(values or {"elements": ["a"], "relations": []})


def _signature(state):
    return state.to_psi().to_dict()


def test_same_state_is_independent_of_global_context(monkeypatch):
    external = {"value": 0}

    def generate(state):
        # Generator is intentionally state-only; changing unrelated process
        # context must not alter the canonical result.
        return [state]

    def test(state):
        return True

    engine = EndogenousEvolution(generate=generate, test=test)

    external["value"] = 1
    first = _signature(engine.evolve(_state()))
    external["value"] = 999999
    second = _signature(engine.evolve(_state()))

    assert first == second


def test_same_state_is_independent_of_random_source(monkeypatch):
    def generate(state):
        return [state]

    def test(state):
        return True

    engine = EndogenousEvolution(generate=generate, test=test)

    monkeypatch.setattr(random, "random", lambda: 0.0)
    first = _signature(engine.evolve(_state()))
    monkeypatch.setattr(random, "random", lambda: 1.0)
    second = _signature(engine.evolve(_state()))

    assert first == second


def test_same_state_is_independent_of_wall_clock(monkeypatch):
    def generate(state):
        return [state]

    def test(state):
        return True

    engine = EndogenousEvolution(generate=generate, test=test)

    monkeypatch.setattr(time, "time", lambda: 1.0)
    first = _signature(engine.evolve(_state()))
    monkeypatch.setattr(time, "time", lambda: 9999999999.0)
    second = _signature(engine.evolve(_state()))

    assert first == second


def test_repeated_execution_with_identical_state_has_identical_result():
    def generate(state):
        return [state]

    def test(state):
        return True

    engine = EndogenousEvolution(generate=generate, test=test)
    results = [_signature(engine.evolve(_state())) for _ in range(5)]

    assert all(result == results[0] for result in results)
