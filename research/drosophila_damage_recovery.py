"""Damage/recovery experiments for the Drosophila-inspired Ψ adapter.

This module deliberately contains an experiment harness, not a repair oracle.
The harness removes relations and observes what the existing local dynamics
can do. It does not prescribe which missing relation must be restored.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_principles import LIFState, Synapse, lif_step, plasticity_step, propagate


@dataclass(frozen=True)
class DamageResult:
    before: tuple[Synapse, ...]
    damaged: tuple[Synapse, ...]
    after: tuple[Synapse, ...]
    active_nodes: tuple[str, ...]


def remove_relation(relations: tuple[Synapse, ...], source: str, target: str) -> tuple[Synapse, ...]:
    """Apply the experimental damage operator."""
    return tuple(r for r in relations if not (r.source == source and r.target == target))


def local_recovery_step(
    relations: tuple[Synapse, ...],
    states: Mapping[str, LIFState],
) -> tuple[Synapse, ...]:
    """Run one endogenous local plasticity step; no target graph is supplied."""
    inputs = propagate(states, relations)
    next_states = {
        node: lif_step(states[node], inputs[node])
        for node in states
    }
    return plasticity_step(relations, next_states)


def run_damage_experiment(
    relations: tuple[Synapse, ...],
    states: Mapping[str, LIFState],
    *,
    damaged_source: str,
    damaged_target: str,
) -> DamageResult:
    """Damage one relation and perform one local recovery attempt."""
    damaged = remove_relation(relations, damaged_source, damaged_target)
    after = local_recovery_step(damaged, states)
    active = tuple(sorted(node for node, state in states.items() if state.spiked))
    return DamageResult(relations, damaged, after, active)
