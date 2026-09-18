"""Canonical admission chain tying existing contracts together."""
from __future__ import annotations

from dataclasses import dataclass

from .commit_contract import CommitResult, commit_once
from .gas import GasBudget
from .history import AppendOnlyHistory, TransitionRecord
from .provenance import Provenance, attach_provenance
from .safety import SafetyGate


@dataclass(frozen=True)
class CanonicalAdmission:
    history: AppendOnlyHistory
    record: TransitionRecord
    provenance: Provenance
    gas: GasBudget


def admit_transition(
    history: AppendOnlyHistory,
    record: TransitionRecord,
    provenance: Provenance,
    current_state,
    next_state,
    operation_count: int,
    gas_costs: tuple[int, ...],
    gate: SafetyGate | None = None,
    gas_limit: int = 20,
) -> CommitResult:
    gate = gate or SafetyGate(max_operations=gas_limit)
    gate.require(operation_count)
    if len(gas_costs) != operation_count:
        raise ValueError("operation/cost cardinality mismatch")
    budget = GasBudget(gas_limit)
    for cost in gas_costs:
        budget = budget.charge(cost)
    attach_provenance(record, provenance)
    return commit_once(history, record, current_state, next_state)
