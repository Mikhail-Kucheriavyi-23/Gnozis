import pytest

from core.execution_contract import validate_execution_plan
from core.safety import SafetyGate


def test_execution_plan_requires_safety_and_gas():
    budget = validate_execution_plan(2, (1, 2))
    assert budget.used == 3


def test_execution_plan_fails_on_operation_limit():
    with pytest.raises(PermissionError):
        validate_execution_plan(21, tuple([1] * 21))


def test_execution_plan_fails_on_gas_limit():
    with pytest.raises(ValueError, match="exhausted"):
        validate_execution_plan(2, (15, 6), gas_limit=20)


def test_execution_plan_honors_hard_stop():
    with pytest.raises(PermissionError):
        validate_execution_plan(1, (1,), SafetyGate(hard_stop=True))


from core.execution_contract import (
    execution_input_from_psi,
    execution_input_identity,
    state_digest,
    state_id,
    verify_execution_input,
)
from core.state import Psi


def test_execution_input_binds_exact_state_identity_and_digest():
    psi_a = Psi(x=("a",), relations=())
    psi_b = Psi(x=("b",), relations=())
    execution_input = execution_input_from_psi(
        psi_a, input_type="canonical-step", content_digest="content-a"
    )

    verify_execution_input(execution_input, psi_a)
    with pytest.raises(ValueError, match="state_id"):
        verify_execution_input(execution_input, psi_b)


def test_execution_input_identity_changes_with_content_digest():
    psi = Psi(x=("a",), relations=())
    a = execution_input_from_psi(psi, input_type="canonical-step", content_digest="a")
    b = execution_input_from_psi(psi, input_type="canonical-step", content_digest="b")
    assert a.state_id == state_id(psi)
    assert a.state_digest == state_digest(psi)
    assert execution_input_identity(a) != execution_input_identity(b)
