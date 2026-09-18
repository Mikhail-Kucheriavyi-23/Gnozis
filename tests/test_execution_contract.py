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
