from research.drosophila_principles import LIFState, Synapse
from research.novel_topology_generation import generate_local_relations


def test_coactive_nodes_can_create_a_new_relation():
    states = {"a": LIFState(spiked=True), "b": LIFState(spiked=True)}
    relations = ()
    evolved = generate_local_relations(states, relations)
    assert Synapse("a", "b", 0.05) in evolved
    assert Synapse("b", "a", 0.05) in evolved


def test_generation_does_not_duplicate_existing_relations():
    states = {"a": LIFState(spiked=True), "b": LIFState(spiked=True)}
    relations = (Synapse("a", "b", 0.2),)
    evolved = generate_local_relations(states, relations)
    assert evolved.count(Synapse("a", "b", 0.2)) == 1


def test_inactive_nodes_do_not_generate_new_topology():
    states = {"a": LIFState(spiked=True), "b": LIFState()}
    assert generate_local_relations(states, ()) == ()
