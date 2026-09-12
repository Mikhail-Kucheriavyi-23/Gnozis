from research.drosophila_principles import LIFState, Synapse
from research.persistence_experiment import run_persistence


def test_persistence_records_each_local_step():
    states = {"a": LIFState(), "b": LIFState()}
    relations = (Synapse("a", "b", 0.5), Synapse("b", "a", 0.5))
    history = run_persistence(states, relations, external_input={"a": 1.1}, steps=5)
    assert len(history) == 5
    assert all(0.0 <= step.viability <= 1.0 for step in history)


def test_persistence_has_no_global_clock_state_or_external_selector():
    states = {"a": LIFState(), "b": LIFState()}
    relations = (Synapse("a", "b", 0.5),)
    history = run_persistence(states, relations, steps=3)
    assert len(history) == 3
    assert all(isinstance(step.states, dict) for step in history)
