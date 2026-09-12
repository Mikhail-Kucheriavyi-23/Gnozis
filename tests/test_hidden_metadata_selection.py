"""Adversarial checks that selection is not controlled by hidden metadata."""

from core import State
from core.evolution import select_next_state


def _psi_state(relations, **extra):
    values = {"x": (), "relations": relations, **extra}
    return State(values=values)


def test_selection_uses_psi_not_unrelated_metadata():
    initial = _psi_state(())

    # Same canonical Ψ content; metadata is deliberately unrelated to Ψ.
    left = _psi_state((("a", "b"),), metadata={"source": "left"})
    right = _psi_state((("a", "b"),), metadata={"source": "right"})

    def test(_state):
        return True

    selected_lr = select_next_state(initial, lambda _s: (left, right), test)
    selected_rl = select_next_state(initial, lambda _s: (right, left), test)

    assert selected_lr.to_psi() == selected_rl.to_psi()
    assert selected_lr.to_psi() == left.to_psi()


def test_selection_is_not_affected_by_object_identity():
    initial = _psi_state(())
    candidate_a = _psi_state((("a", "b"),))
    candidate_b = _psi_state((("a", "b"),))

    def test(_state):
        return True

    result_a = select_next_state(initial, lambda _s: (candidate_a,), test)
    result_b = select_next_state(initial, lambda _s: (candidate_b,), test)

    assert result_a.to_psi() == result_b.to_psi()
