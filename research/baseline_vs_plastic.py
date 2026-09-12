"""Controlled baseline-vs-plastic comparison for the Drosophila research adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_principles import LIFState, Synapse, lif_step, propagate
from .novel_topology_generation import generate_novel_relations
from .viability import viability


@dataclass(frozen=True)
class ComparisonStep:
    states: dict[str, LIFState]
    relations: tuple[Synapse, ...]
    viability: float


def run_variant(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    inputs: tuple[Mapping[str, float], ...],
    plastic: bool,
) -> tuple[ComparisonStep, ...]:
    current = dict(states)
    current_relations = tuple(relations)
    history: list[ComparisonStep] = []
    for external in inputs:
        recurrent = propagate(current, current_relations)
        current = {
            node: lif_step(current[node], external.get(node, 0.0) + recurrent.get(node, 0.0))
            for node in current
        }
        if plastic:
            current_relations = tuple(current_relations) + tuple(
                generate_novel_relations(current, current_relations)
            )
        history.append(ComparisonStep(current, current_relations, viability(current, current_relations)))
    return tuple(history)


def compare_baseline_and_plastic(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    inputs: tuple[Mapping[str, float], ...],
) -> tuple[tuple[ComparisonStep, ...], tuple[ComparisonStep, ...]]:
    """Run identical inputs through baseline and plastic variants."""
    return (
        run_variant(states, relations, inputs=inputs, plastic=False),
        run_variant(states, relations, inputs=inputs, plastic=True),
    )
