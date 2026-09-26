from core.execution import CanonicalExecutor
from core.history import AppendOnlyHistory
from core.psi_transition import PsiTransition
from core.state import Psi


def test_canonical_step_binds_candidate_to_transition_result():
    psi = Psi((1,), ())
    transition = PsiTransition(lambda x, r: (tuple(x) + (2,), r))
    executor = CanonicalExecutor(
        history=AppendOnlyHistory(),
        kernel_version="test",
    )

    result = executor.step(psi, transition)

    assert result.psi == transition(psi)
    assert result.psi == Psi((1, 2), ())
