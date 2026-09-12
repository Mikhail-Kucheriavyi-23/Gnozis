"""Reproducible baseline/random/plastic benchmark runner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .baseline_vs_plastic import ComparisonStep, run_variant
from .drosophila_principles import LIFState, Synapse
from .random_matched import generate_matched_random_relations


@dataclass(frozen=True)
class BenchmarkResult:
    variant: str
    steps: tuple[ComparisonStep, ...]

    @property
    def final_viability(self) -> float:
        return self.steps[-1].viability if self.steps else 0.0

    @property
    def relation_count(self) -> int:
        return len(self.steps[-1].relations) if self.steps else 0


def recovery_gain(before: float, damaged: float, recovered: float) -> float:
    """Absolute recovery from the damaged state."""
    return recovered - damaged


def run_benchmark(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    inputs: tuple[Mapping[str, float], ...],
    seed: int,
) -> tuple[BenchmarkResult, BenchmarkResult, BenchmarkResult]:
    """Run identical inputs through baseline, matched random, and plastic variants.

    The random control is generated internally from the same node set and exact
    initial relation budget as the supplied topology. It has no access to
    viability or to the plastic variant's outcome.
    """
    nodes = tuple(states.keys())
    matched = generate_matched_random_relations(
        nodes,
        len(relations),
        seed=seed,
        weight=relations[0].weight if relations else 0.05,
    )
    baseline = run_variant(states, relations, inputs=inputs, plastic=False)
    random_control = run_variant(states, matched, inputs=inputs, plastic=False)
    plastic = run_variant(states, relations, inputs=inputs, plastic=True)
    return (
        BenchmarkResult("baseline", baseline),
        BenchmarkResult("random_matched", random_control),
        BenchmarkResult("drosophila_plastic", plastic),
    )
