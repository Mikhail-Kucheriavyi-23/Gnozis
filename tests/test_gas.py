import pytest

from core.gas import GasBudget, bounded_cost


def test_gas_budget_charges_deterministically():
    budget = bounded_cost(5, (1, 2))
    assert budget.used == 3
    assert budget.remaining == 2


def test_gas_budget_fails_closed():
    with pytest.raises(ValueError, match="exhausted"):
        bounded_cost(3, (1, 2, 1))


def test_invalid_budget_is_rejected():
    with pytest.raises(ValueError):
        GasBudget(2, 3)
