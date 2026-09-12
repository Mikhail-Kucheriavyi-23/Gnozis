"""Budget-matched benchmark protocol for baseline, random, and plastic variants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .baseline_vs_plastic import run_variant, ComparisonStep
from .drosophila_principles import LIFState, Synapse


@dataclass(frozen=True)
class BenchmarkResult:
    baseline: tuple[ComparisonStep, ...]
    random_matched: tuple[ComparisonStep, ...]
    plastic: tuple[ComparisonStep, ...]


def run_controlled_benchmark(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    inputs: tuple[Mapping[str, float], ...],
    random_matched_relations: tuple[Synapse, ...],
) -> BenchmarkResult:
    """Run three variants with identical inputs.

    The random-matched relation set is supplied by the caller so that the
    benchmark does not hide a randomization policy inside the measurement.
    """
    baseline = run_variant(states, relations, inputs=inputs, plastic=False)
    random_matched = run_variant(
        states, random_matched_relations, inputs=inputs, plastic=False
    )
    plastic = run_variant(states, relations, inputs=inputs, plastic=True)
    return BenchmarkResult(baseline, random_matched, plastic)


def recovery_gain(before_damage: float, after_recovery: float) -> float:
    return after_recovery - before_damage
