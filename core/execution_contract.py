"""Canonical execution-boundary contract without introducing a second executor."""
from __future__ import annotations
from dataclasses import dataclass

from .gas import GasBudget
from .safety import SafetyGate


@dataclass(frozen=True)
class ExecutionPlan:
    operation_count: int
    gas_costs: tuple[int, ...]

    def validate(self, gate: SafetyGate, gas_limit: int) -> GasBudget:
        if len(self.gas_costs) != self.operation_count:
            raise ValueError("operation/cost cardinality mismatch")
        gate.require(self.operation_count)
        budget = GasBudget(gas_limit)
        for cost in self.gas_costs:
            budget = budget.charge(cost)
        return budget


def validate_execution_plan(
    operation_count: int,
    gas_costs: tuple[int, ...],
    gate: SafetyGate | None = None,
    gas_limit: int = 20,
) -> GasBudget:
    plan = ExecutionPlan(operation_count, gas_costs)
    return plan.validate(gate or SafetyGate(max_operations=gas_limit), gas_limit)
