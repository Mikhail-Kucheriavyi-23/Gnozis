from research.drosophila_damage_recovery import remove_relation, run_damage_experiment
from research.drosophila_principles import LIFState, Synapse


def test_damage_is_structural_and_local():
    relations = (Synapse("a", "b", 0.5), Synapse("b", "c", 0.5))
    damaged = remove_relation(relations, "a", "b")
    assert damaged == (Synapse("b", "c", 0.5),)


def test_damage_experiment_does_not_invent_a_target_relation():
    relations = (Synapse("a", "b", 0.5), Synapse("b", "c", 0.5), Synapse("c", "a", 0.5))
    states = {"a": LIFState(spiked=True), "b": LIFState(), "c": LIFState()}
    result = run_damage_experiment(
        relations, states, damaged_source="a", damaged_target="b"
    )
    assert Synapse("a", "b", 0.5) not in result.damaged
    assert all(r.source != "a" or r.target != "b" for r in result.after)


def test_damage_experiment_preserves_observability_of_existing_structure():
    relations = (Synapse("a", "b", 0.5), Synapse("b", "c", 0.5), Synapse("c", "a", 0.5))
    states = {"a": LIFState(spiked=True), "b": LIFState(), "c": LIFState()}
    result = run_damage_experiment(
        relations, states, damaged_source="a", damaged_target="b"
    )
    assert result.before == relations
    assert len(result.damaged) == 2
    assert set(result.active_nodes) == {"a"}
