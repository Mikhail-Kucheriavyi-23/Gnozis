"""Adversarial checks for endogenous evolution of the relation component R."""

from core import State
from core.evolution import evolutionary_transition


def _psi_state(relations):
    return State(values={"x": (), "relations": relations})


def _transition(candidates):
    def generate(_state):
        return tuple(candidates)

    return evolutionary_transition(generate, lambda _candidate: True)


def test_relations_can_evolve_to_empty_set():
    initial = _psi_state((("a", "b"),))
    reduced = _psi_state(())

    result = _transition((reduced,))(initial)

    assert result.to_psi().relations == ()
    assert initial.to_psi().relations == (("a", "b"),)


def test_empty_relations_can_evolve_to_nonempty_set():
    initial = _psi_state(())
    expanded = _psi_state((("a", "b"),))

    result = _transition((expanded,))(initial)

    assert result.to_psi().relations == (("a", "b"),)


def test_relation_change_is_realized_through_generate_test_select_cycle():
    initial = _psi_state((("a", "b"),))
    rejected = _psi_state((("bad", "relation"),))
    accepted = _psi_state(())

    def generate(_state):
        return (rejected, accepted)

    def test(candidate):
        return candidate.to_psi().relations == ()

    result = evolutionary_transition(generate, test)(initial)

    assert result == accepted
    assert result.to_psi().relations == ()
