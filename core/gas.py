"""Deterministic gas/resource bound for bounded autonomous operations."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GasBudget:
    limit: int
    used: int = 0

    def __post_init__(self) -> None:
        if self.limit < 0 or self.used < 0 or self.used > self.limit:
            raise ValueError("invalid gas budget")

    @property
    def remaining(self) -> int:
        return self.limit - self.used

    def charge(self, cost: int) -> "GasBudget":
        if cost < 0:
            raise ValueError("gas cost must be non-negative")
        if cost > self.remaining:
            raise ValueError("gas budget exhausted")
        return GasBudget(self.limit, self.used + cost)


def bounded_cost(limit: int, costs: tuple[int, ...]) -> GasBudget:
    budget = GasBudget(limit)
    for cost in costs:
        budget = budget.charge(cost)
    return budget
