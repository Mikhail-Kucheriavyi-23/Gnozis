"""Canonical admission chain tying safety, gas, provenance and persistence."""
from __future__ import annotations

from dataclasses import dataclass

from .commit_contract import CommitResult, commit_once
from .gas import GasBudget
from .history import AppendOnlyHistory, TransitionRecord
from .mutation_guard import guard_transition
from .provenance import Provenance
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
    guard_transition(
        record,
        provenance,
        operation_count=operation_count,
        gas_costs=gas_costs,
        gate=gate,
        gas_limit=gas_limit,
    )
    return commit_once(history, record, current_state, next_state)
