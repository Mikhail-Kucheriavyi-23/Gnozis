"""Reproducible baseline/random/plastic benchmark runner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .baseline_vs_plastic import ComparisonStep, run_variant
from .drosophila_principles import LIFState, Synapse
from .viability import viability


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
    random_relations: tuple[Synapse, ...] | None = None,
) -> tuple[BenchmarkResult, BenchmarkResult, BenchmarkResult]:
    """Run identical inputs through baseline, matched control, and plastic variants."""
    matched = relations if random_relations is None else random_relations
    baseline = run_variant(states, relations, inputs=inputs, plastic=False)
    random_control = run_variant(states, matched, inputs=inputs, plastic=False)
    plastic = run_variant(states, relations, inputs=inputs, plastic=True)
    return (
        BenchmarkResult("baseline", baseline),
        BenchmarkResult("random_matched", random_control),
        BenchmarkResult("drosophila_plastic", plastic),
    )
