import pytest

from core.execution import CanonicalExecutor
from core.history import AppendOnlyHistory
from core.psi_transition import PsiTransition
from core.state import Psi
from core.canonical_boundary import canonicalize_psi


def test_accepted_step_creates_exactly_one_history_record():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition)

    assert result.psi == transition(psi)
    assert len(result.history.records) == 1
    assert result.history.records[0].admitted is True


def test_rejected_step_does_not_create_history_record():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition, test=lambda _: False)

    assert result.psi == psi
    assert result.history.records == ()


def test_step_uses_the_declared_transition_as_candidate_source():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition)

    assert result.psi == Psi((2,), ())
    assert result.psi == transition(psi)
