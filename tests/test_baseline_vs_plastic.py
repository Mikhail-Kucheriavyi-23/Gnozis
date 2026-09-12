from research.baseline_vs_plastic import compare_baseline_and_plastic
from research.drosophila_principles import LIFState, Synapse


def test_baseline_and_plastic_receive_identical_inputs():
    states = {"a": LIFState(), "b": LIFState(), "c": LIFState()}
    relations = (Synapse("a", "b", 0.5), Synapse("b", "a", 0.5))
    inputs = ({"a": 1.0}, {"b": 1.0}, {"c": 1.0})
    baseline, plastic = compare_baseline_and_plastic(states, relations, inputs=inputs)
    assert len(baseline) == len(plastic) == len(inputs)
    assert baseline[0].states == plastic[0].states


def test_plastic_variant_can_expand_relations_while_baseline_cannot():
    states = {"a": LIFState(), "b": LIFState(), "c": LIFState()}
    relations = (Synapse("a", "b", 0.5), Synapse("b", "a", 0.5))
    inputs = ({"a": 1.0}, {"b": 1.0}, {"a": 1.0, "b": 1.0})
    baseline, plastic = compare_baseline_and_plastic(states, relations, inputs=inputs)
    assert len(plastic[-1].relations) >= len(baseline[-1].relations)
