"""Deterministic structural-budget matched random control."""

from __future__ import annotations

import random

from .drosophila_principles import Synapse


def generate_matched_random_relations(
    nodes: tuple[str, ...],
    count: int,
    *,
    seed: int,
    weight: float = 0.05,
) -> tuple[Synapse, ...]:
    """Generate a reproducible random directed topology with an exact edge budget.

    Selection is independent of viability and of the plasticity outcome.
    """
    if count < 0:
        raise ValueError("count must be non-negative")
    candidates = [
        (source, target)
        for source in nodes
        for target in nodes
        if source != target
    ]
    if count > len(candidates):
        raise ValueError("count exceeds available directed non-self edges")
    rng = random.Random(seed)
    selected = rng.sample(candidates, count)
    return tuple(Synapse(source, target, weight) for source, target in selected)
