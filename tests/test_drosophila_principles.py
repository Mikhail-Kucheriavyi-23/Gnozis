from research.drosophila_principles import LIFState, Synapse, lif_step, plasticity_step, propagate, structural_decay


def test_lif_threshold_and_reset_are_local():
    state = lif_step(LIFState(), 1.1)
    assert state.spiked is True
    assert state.potential == 0.0


def test_recurrent_propagation_uses_relation_structure():
    states = {"a": LIFState(spiked=True), "b": LIFState()}
    relations = (Synapse("a", "b", 0.4),)
    assert propagate(states, relations)["b"] == 0.4


def test_coactive_relation_strengthens():
    states = {"a": LIFState(spiked=True), "b": LIFState(spiked=True)}
    relations = (Synapse("a", "b", 0.4),)
    evolved = plasticity_step(relations, states)
    assert evolved == (Synapse("a", "b", 0.45),)


def test_inactive_target_weakens_relation():
    states = {"a": LIFState(spiked=True), "b": LIFState(spiked=False)}
    relations = (Synapse("a", "b", 0.04),)
    evolved = plasticity_step(relations, states)
    assert evolved == (Synapse("a", "b", 0.02),)


def test_relation_can_extinguish_without_external_selector():
    states = {"a": LIFState(spiked=True), "b": LIFState(spiked=False)}
    relations = (Synapse("a", "b", 0.02),)
    assert plasticity_step(relations, states) == ()


def test_structural_decay_is_monotone_and_removes_zero_weight_edges():
    relations = (Synapse("a", "b", 0.01), Synapse("b", "c", 0.0))
    evolved = structural_decay(relations, rate=0.5)
    assert len(evolved) == 1
    assert evolved[0].weight < 0.01
