import pytest

from core.admission import admit
from core.execution import CanonicalExecutor
from core.history import AppendOnlyHistory
from core.proof import ProofObligation
from core.psi_transition import PsiTransition
from core.state import Psi


def test_canonical_step_rejects_admission_for_different_candidate():
    psi = Psi((1,), ())
    transition = PsiTransition(lambda x, r: (tuple(x) + (2,), r))
    wrong = Psi((1, 999), ())
    proof = ProofObligation(
        passed=True,
        invariant=True,
        viable=True,
        evidence={"test": "binding"},
    )

    executor = CanonicalExecutor(
        history=AppendOnlyHistory(),
        kernel_version="test",
    )

    with pytest.raises(ValueError, match="does not match PsiTransition result"):
        executor.step(psi, transition, admit(wrong, proof))
