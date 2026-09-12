"""No-input self-support experiment for the Ψ research adapter.

A finite initialization is supplied once. After that, no external input is
provided. The experiment records whether recurrent structure alone sustains
activity and viability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_principles import LIFState, Synapse, lif_step, propagate
from .viability import viability


@dataclass(frozen=True)
class SelfSupportStep:
    states: dict[str, LIFState]
    viability: float
    active_count: int


def run_no_input_self_support(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    steps: int = 20,
) -> tuple[SelfSupportStep, ...]:
    """Remove external input after initialization and observe local recurrence."""
    current = dict(states)
    history: list[SelfSupportStep] = []
    for _ in range(max(0, steps)):
        recurrent = propagate(current, relations)
        current = {
            node: lif_step(current[node], recurrent.get(node, 0.0))
            for node in current
        }
        active_count = sum(state.spiked for state in current.values())
        history.append(
            SelfSupportStep(current, viability(current, relations), active_count)
        )
    return tuple(history)
