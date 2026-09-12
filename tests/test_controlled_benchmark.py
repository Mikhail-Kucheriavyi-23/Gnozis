from research.controlled_benchmark import recovery_gain, run_controlled_benchmark
from research.drosophila_principles import LIFState, Synapse


def test_three_way_benchmark_uses_identical_inputs():
    states = {"a": LIFState(), "b": LIFState(), "c": LIFState()}
    base = (Synapse("a", "b", 0.5), Synapse("b", "a", 0.5))
    matched = (Synapse("a", "c", 0.5), Synapse("c", "a", 0.5))
    result = run_controlled_benchmark(
        states, base, inputs=(("a", 1.0),), random_matched_relations=matched
    )
    assert len(result.baseline) == len(result.random_matched) == len(result.plastic) == 1


def test_recovery_gain_is_difference():
    assert recovery_gain(0.25, 0.75) == 0.5
