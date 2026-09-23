from research.drosophila_principles import LIFState, Synapse
from research.self_recovery_experiment import finite_pulse_damage_recovery


def test_external_input_is_only_present_during_warmup():
    states = {"a": LIFState(), "b": LIFState()}
    relations = (Synapse("a", "b", 0.8), Synapse("b", "a", 0.8))
    history = finite_pulse_damage_recovery(
        states, relations, initial_input={"a": 1.1},
        damage_source="a", damage_target="b", warmup_steps=1, recovery_steps=3,
    )
    assert len(history) == 4


def test_damage_removes_relation_before_recovery_phase():
    states = {"a": LIFState(), "b": LIFState()}
    relations = (Synapse("a", "b", 0.8), Synapse("b", "a", 0.8))
    history = finite_pulse_damage_recovery(
        states, relations, initial_input={"a": 1.1},
        damage_source="a", damage_target="b", warmup_steps=1, recovery_steps=1,
    )
    assert all(not (r.source == "a" and r.target == "b") for r in history[-1].relations)
