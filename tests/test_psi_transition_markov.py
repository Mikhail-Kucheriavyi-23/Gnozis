from core.psi_transition import PsiTransition
from core.state import Psi


def test_transition_result_is_independent_of_unrelated_closure_mutation():
    external = {"noise": 0}

    def transition(x, relations):
        return (tuple(x) + (external["noise"],), relations)

    op = PsiTransition(transition)
    psi = Psi((1,), ())

    first = op(psi)
    external["noise"] = 999
    second = op(psi)

    # This intentionally demonstrates the boundary: the current callable
    # is NOT Markov-sufficient if it reads undeclared closure state.
    assert first != second
