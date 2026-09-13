"""Contract tests for the canonical Ψ Engine boundary."""

from core import Psi, PsiEngine


def test_engine_state_is_only_psi():
    engine = PsiEngine(Psi(frozenset({"a"}), frozenset()))
    assert engine.psi.X == frozenset({"a"})
    assert engine.psi.R == frozenset()
    assert not hasattr(engine, "hidden")


def test_engine_transition_receives_only_psi():
    seen = []

    def transition(psi):
        seen.append(psi)
        return psi

    engine = PsiEngine(Psi(frozenset({"a"}), frozenset()), transition=transition)
    engine.step()

    assert len(seen) == 1
    assert isinstance(seen[0], Psi)
    assert not hasattr(seen[0], "hidden")


def test_engine_rejects_non_psi_transition_result():
    def bad_transition(_psi):
        return {"X": {"a"}, "R": set()}

    engine = PsiEngine(Psi(frozenset({"a"}), frozenset()), transition=bad_transition)

    try:
        engine.step()
    except TypeError:
        pass
    else:
        raise AssertionError("canonical Ψ Engine accepted a non-Ψ transition result")
