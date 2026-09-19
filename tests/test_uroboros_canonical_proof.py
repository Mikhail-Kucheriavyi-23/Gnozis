from core.psi_transition import make_psi_transition
from core.state import State
from core.uroboros import Uroboros


def test_canonical_uroboros_uses_fundamental_proof_regime():
    transition = make_psi_transition(lambda psi: psi)
    uro = Uroboros.canonical(transition=transition, state=State())

    admission = uro._canonical_admission()

    assert admission.accepted is True
    assert admission.proof.evidence["regime"] == "fundamental"
    assert admission.proof.evidence["viability"] == "not_applicable"
    assert admission.proof.viable is False
