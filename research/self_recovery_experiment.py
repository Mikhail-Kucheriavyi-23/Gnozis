"""Finite-pulse damage/recovery protocol for the Ψ research adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_damage_recovery import local_recovery_step, remove_relation
from .drosophila_principles import LIFState, Synapse, lif_step, propagate
from .viability import viability


@dataclass(frozen=True)
class RecoveryObservation:
    states: dict[str, LIFState]
    relations: tuple[Synapse, ...]
    viability: float


def finite_pulse_damage_recovery(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    initial_input: Mapping[str, float],
    damage_source: str,
    damage_target: str,
    warmup_steps: int = 1,
    recovery_steps: int = 10,
) -> tuple[RecoveryObservation, ...]:
    """Pulse once, remove external input, damage one relation, then observe recovery."""
    current_states = dict(states)
    current_relations = relations
    history: list[RecoveryObservation] = []
    for _ in range(max(0, warmup_steps)):
        recurrent = propagate(current_states, current_relations)
        current_states = {node: lif_step(current_states[node], initial_input.get(node, 0.0) + recurrent.get(node, 0.0)) for node in current_states}
        history.append(RecoveryObservation(current_states, current_relations, viability(current_states, current_relations)))
    current_relations = remove_relation(current_relations, damage_source, damage_target)
    for _ in range(max(0, recovery_steps)):
        current_relations = local_recovery_step(current_relations, current_states)
        recurrent = propagate(current_states, current_relations)
        current_states = {node: lif_step(current_states[node], recurrent.get(node, 0.0)) for node in current_states}
        history.append(RecoveryObservation(current_states, current_relations, viability(current_states, current_relations)))
    return tuple(history)
