from core.psi_transition import make_psi_transition
from core.refinement import refine
from core.state import Psi


def identity():
    return make_psi_transition(lambda x, r: (x, r))


def add_marker():
    return make_psi_transition(lambda x, r: (tuple(x) + ("m",), r))


def relation(a, b):
    return set(a.x).issubset(set(b.x)) and a.relations == b.relations


def test_refinement_accepts_forward_witness():
    psi = Psi(x=("a",), relations=())
    proof = refine(identity(), add_marker(), relation, [psi])
    assert proof.holds()


def test_refinement_rejects_failed_forward_witness():
    psi = Psi(x=("a",), relations=())
    old = add_marker()
    new = identity()
    proof = refine(old, new, relation, [psi])
    assert not proof.holds()
