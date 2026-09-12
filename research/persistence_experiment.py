"""Temporal persistence experiment for Ψ research."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_principles import LIFState, Synapse, lif_step, propagate
from .viability import viability


@dataclass(frozen=True)
class PersistenceStep:
    states: dict[str, LIFState]
    viability: float


def run_persistence(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    external_input: Mapping[str, float] | None = None,
    *,
    steps: int = 10,
) -> tuple[PersistenceStep, ...]:
    """Run local dynamics for multiple steps and record structural viability."""
    current = dict(states)
    inputs = dict(external_input or {})
    history: list[PersistenceStep] = []
    for _ in range(max(0, steps)):
        recurrent = propagate(current, relations)
        current = {
            node: lif_step(current[node], inputs.get(node, 0.0) + recurrent.get(node, 0.0))
            for node in current
        }
        history.append(PersistenceStep(current, viability(current, relations)))
    return tuple(history)
