from research.drosophila_principles import LIFState, Synapse
from research.viability import viability


def test_connected_active_structure_is_viable():
    states = {"a": LIFState(spiked=True), "b": LIFState(spiked=True)}
    relations = (Synapse("a", "b", 0.5),)
    assert viability(states, relations) == 1.0


def test_disconnected_active_structure_is_partially_viable():
    states = {
        "a": LIFState(spiked=True),
        "b": LIFState(spiked=True),
        "c": LIFState(spiked=True),
    }
    relations = (Synapse("a", "b", 0.5),)
    assert viability(states, relations) == 2 / 3


def test_no_active_nodes_are_non_viable():
    states = {"a": LIFState(), "b": LIFState()}
    assert viability(states, ()) == 0.0
