import pytest

from core.canonical_boundary import canonicalize_psi
from core.execution import CanonicalExecutor
from core.execution_contract import execution_input_from_psi
from core.history import AppendOnlyHistory
from core.psi_transition import PsiTransition
from core.state import Psi


def execution_input(psi: Psi):
    return execution_input_from_psi(
        psi,
        input_type="psi_transition",
        content_digest="test-content",
    )


def test_accepted_step_creates_exactly_one_history_record():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition, execution_input(psi))

    assert result.psi == transition(psi)
    assert len(result.history.records) == 1
    assert result.history.records[0].admitted is True


def test_rejected_step_does_not_create_history_record():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(
        psi,
        transition,
        execution_input(psi),
        test=lambda _: False,
    )

    assert result.psi == psi
    assert result.history.records == ()


def test_step_uses_the_declared_transition_as_candidate_source():
    psi = Psi(x=(1,), relations=())
    transition = PsiTransition(lambda x, r: (x + (1,), r))
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    result = executor.step(psi, transition, execution_input(psi))

    assert result.psi == Psi((1, 1), ())
    assert result.psi == transition(psi)


def test_step_rejects_state_substitution_before_transition_execution():
    declared_state = Psi(x=("declared",), relations=())
    substituted_state = Psi(x=("substituted",), relations=())
    calls = []

    transition = PsiTransition(
        lambda x, r: (calls.append(x) or x, r),
    )
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    with pytest.raises(ValueError, match="state_(id|digest)"):
        executor.step(substituted_state, transition, execution_input(declared_state))

    assert calls == []
    assert executor.history.records == ()


def test_step_rejects_tampered_state_digest():
    psi = Psi(x=(1,), relations=())
    declared = execution_input(psi)
    tampered = type(declared)(
        input_type=declared.input_type,
        state_id=declared.state_id,
        state_digest="0" * len(declared.state_digest),
        content_digest=declared.content_digest,
    )
    executor = CanonicalExecutor(AppendOnlyHistory(), "test-kernel")

    with pytest.raises(ValueError, match="state_digest"):
        executor.step(psi, PsiTransition(lambda x, r: (x + (1,), r)), tampered)

    assert executor.history.records == ()
