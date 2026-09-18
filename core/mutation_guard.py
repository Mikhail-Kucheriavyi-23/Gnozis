"""Shared pre-commit safety, gas and provenance guard.

This layer composes with Ψ-specific SemanticCommit without becoming the
semantic transition authority itself.
"""
from __future__ import annotations

from .gas import GasBudget
from .history import TransitionRecord
from .provenance import Provenance, attach_provenance
from .safety import SafetyGate


def guard_transition(
    record: TransitionRecord,
    provenance: Provenance,
    *,
    operation_count: int,
    gas_costs: tuple[int, ...],
    gate: SafetyGate | None = None,
    gas_limit: int = 20,
) -> None:
    gate = gate or SafetyGate(max_operations=gas_limit)
    gate.require(operation_count)
    if len(gas_costs) != operation_count:
        raise ValueError("operation/cost cardinality mismatch")
    budget = GasBudget(gas_limit)
    for cost in gas_costs:
        budget = budget.charge(cost)
    attach_provenance(record, provenance)
