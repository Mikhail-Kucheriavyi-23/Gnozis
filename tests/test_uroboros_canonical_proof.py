from core.psi_transition import PsiTransition
from core.state import State
from core.state import Psi
from core.proof import prove_fundamental_transition


def test_canonical_uroboros_uses_fundamental_proof_regime():
    psi = Psi((1,), ())
    transition = PsiTransition(lambda x, r: (x, r))
    state = State.from_psi(psi)
    candidate = transition(psi)
    proof = prove_fundamental_transition(
        state,
        State.from_psi(candidate),
        lambda _: True,
    )

    assert proof.passed is True
    assert proof.evidence["regime"] == "fundamental"
    assert proof.evidence["viability"] == "not_applicable"
    assert proof.viable is False
