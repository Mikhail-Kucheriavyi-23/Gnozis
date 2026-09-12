from research.drosophila_principles import LIFState, Synapse
from research.test_repeated_damage import repeated_damage


def test_repeated_damage_keeps_only_structural_state_between_trials():
    relations = (
        Synapse("a", "b", 0.5),
        Synapse("b", "c", 0.5),
        Synapse("c", "a", 0.5),
    )
    states = {"a": LIFState(spiked=True), "b": LIFState(), "c": LIFState()}
    trials = repeated_damage(relations, states, "a", "b", repeats=2)
    assert len(trials) == 2
    assert trials[0].damaged == trials[1].relations_before


def test_identical_damage_is_not_allowed_to_use_a_repair_oracle():
    relations = (Synapse("a", "b", 0.5), Synapse("b", "a", 0.5))
    states = {"a": LIFState(spiked=True), "b": LIFState()}
    trials = repeated_damage(relations, states, "a", "b", repeats=2)
    assert all(Synapse("a", "b", 0.5) not in trial.damaged for trial in trials)
