from core.dynamics import closure, fixed_point
from core.psi_transition import make_psi_transition
from core.state import Psi


def identity():
    return make_psi_transition(lambda x, r: (x, r))


def add_marker():
    return make_psi_transition(lambda x, r: (tuple(x) + ("m",), r))


def test_identity_is_closed_and_fixed_on_witness():
    psi = Psi(x=("a",), relations=())
    transition = identity()
    invariant = lambda p: "a" in p.x
    assert closure(transition, invariant, [psi]).holds()
    assert fixed_point(transition, [psi]).holds()


def test_marker_transition_can_be_closed_but_not_fixed():
    psi = Psi(x=("a",), relations=())
    transition = add_marker()
    invariant = lambda p: "a" in p.x
    assert closure(transition, invariant, [psi]).holds()
    assert not fixed_point(transition, [psi]).holds()
