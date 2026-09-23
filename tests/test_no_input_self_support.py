from research.drosophila_principles import LIFState, Synapse
from research.no_input_self_support import run_no_input_self_support


def test_external_input_is_not_present_after_initialization():
    states = {"a": LIFState(spiked=True), "b": LIFState()}
    relations = (Synapse("a", "b", 1.0), Synapse("b", "a", 1.0))
    history = run_no_input_self_support(states, relations, steps=5)
    assert len(history) == 5


def test_self_support_is_measured_not_assumed():
    states = {"a": LIFState(spiked=True), "b": LIFState()}
    relations = (Synapse("a", "b", 0.2), Synapse("b", "a", 0.2))
    history = run_no_input_self_support(states, relations, steps=10)
    assert all(0.0 <= step.viability <= 1.0 for step in history)
    assert all(step.active_count >= 0 for step in history)
