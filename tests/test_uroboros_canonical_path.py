from core.psi_transition import PsiTransition
from core.state import State
from core.uroboros import Uroboros


def test_uroboros_canonical_path_uses_explicit_psi_transition():
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    uroboros = Uroboros.canonical(
        transition=transition,
        state=State.from_psi(__import__("core.state", fromlist=["Psi"]).Psi((1,), ())),
        kernel_version="test",
    )

    result = uroboros.step()

    assert result.state.to_psi().x == (1, 1)
    assert result.psi_transition is transition
    assert len(result.executor.history.records) == 1
