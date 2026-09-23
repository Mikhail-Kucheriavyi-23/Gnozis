"""Minimal SPT acceptance metrics for the research benchmark.

This module deliberately does not modify core state or choose an outcome.
It only evaluates recorded baseline/random/plastic viability values under
an explicitly matched structural budget.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SPTResult:
    baseline: float
    random_matched: float
    plastic: float
    random_budget: int
    initial_budget: int

    @property
    def matched_budget(self) -> bool:
        return self.random_budget == self.initial_budget

    @property
    def plastic_over_random(self) -> float:
        return self.plastic - self.random_matched

    @property
    def accepted(self) -> bool:
        return self.matched_budget and self.plastic > self.random_matched


def evaluate_spt(
    baseline: Sequence[float],
    random_matched: Sequence[float],
    plastic: Sequence[float],
    *,
    random_budget: int,
    initial_budget: int,
) -> SPTResult:
    """Evaluate final viability using the last recorded benchmark value."""
    if not baseline or not random_matched or not plastic:
        raise ValueError("all benchmark series must be non-empty")
    return SPTResult(
        baseline=float(baseline[-1]),
        random_matched=float(random_matched[-1]),
        plastic=float(plastic[-1]),
        random_budget=random_budget,
        initial_budget=initial_budget,
    )
