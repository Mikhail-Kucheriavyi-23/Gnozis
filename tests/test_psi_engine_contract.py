"""Contract tests for the canonical Ψ Engine boundary."""

import pytest

from core import Psi, PsiEngine


def make_psi() -> Psi:
    return Psi(frozenset({"a"}), frozenset())


def test_engine_accepts_only_psi_as_step_state():
    def transition(psi):
        return psi

    engine = PsiEngine(transition=transition)
    result = engine.step(make_psi())

    assert isinstance(result, Psi)
    assert result.x == frozenset({"a"})
    assert result.relations == frozenset()

    with pytest.raises(TypeError):
        engine.step({"x": {"a"}, "relations": set()})


def test_engine_transition_receives_only_psi():
    seen = []

    def transition(psi):
        seen.append(psi)
        return psi

    engine = PsiEngine(transition=transition)
    engine.step(make_psi())

    assert len(seen) == 1
    assert isinstance(seen[0], Psi)
    assert not hasattr(seen[0], "hidden")


def test_engine_rejects_non_psi_transition_result():
    def bad_transition(_psi):
        return {"x": {"a"}, "relations": set()}

    engine = PsiEngine(transition=bad_transition)

    with pytest.raises((TypeError, AttributeError)):
        engine.step(make_psi())
