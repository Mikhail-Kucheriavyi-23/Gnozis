from research.drosophila_principles import LIFState, Synapse
from research.novel_damage_experiment import run_novel_damage_trial


def test_unseen_damage_is_not_replaced_by_a_repair_oracle():
    relations = (
        Synapse("a", "b", 0.5),
        Synapse("b", "c", 0.5),
        Synapse("c", "a", 0.5),
    )
    states = {"a": LIFState(spiked=True), "b": LIFState(), "c": LIFState()}
    result = run_novel_damage_trial(relations, states, source="b", target="c")
    assert Synapse("b", "c", 0.5) not in result.damaged
    assert all(not (r.source == "b" and r.target == "c") for r in result.after)


def test_novel_damage_retains_structural_observability():
    relations = (Synapse("a", "b", 0.5), Synapse("b", "c", 0.5))
    states = {"a": LIFState(spiked=True), "b": LIFState(), "c": LIFState()}
    result = run_novel_damage_trial(relations, states, source="b", target="c")
    assert result.removed == ("b", "c")
    assert len(result.damaged) == 1
