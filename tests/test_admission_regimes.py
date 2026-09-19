from core.admission import admit
from core.proof import ProofObligation, prove_fundamental_transition, prove_transition


def test_fundamental_admission_does_not_require_viability():
    current = object()
    candidate = object()
    proof = prove_fundamental_transition(current, candidate, lambda _: True)

    admission = admit(candidate, proof)

    assert admission.accepted is True


def test_fundamental_admission_rejects_failed_invariant():
    current = object()
    candidate = object()
    proof = prove_fundamental_transition(current, candidate, lambda _: False)

    admission = admit(candidate, proof)

    assert admission.accepted is False


def test_evolutionary_admission_requires_viability():
    current = object()
    candidate = object()
    proof = prove_transition(current, candidate, (), lambda _: True)

    admission = admit(candidate, proof)

    assert admission.accepted is False


def test_forged_non_fundamental_proof_cannot_bypass_viability():
    proof = ProofObligation(
        passed=True,
        invariant=True,
        viable=False,
        evidence={},
    )

    admission = admit(object(), proof)

    assert admission.accepted is False
