"""Drosophila-inspired research primitives for GNOSIS.

This module is intentionally outside ``core/``.  It does not copy the
Drosophila brain model or its connectome data.  It extracts only mechanisms
that are useful for testing the Ψ=(X,R) hypothesis:

* leaky activity with a threshold/reset;
* local recurrent interaction through weighted relations;
* activity-dependent structural plasticity;
* relation weakening and extinction (R -> ∅).

The implementation is a small, dependency-free research model.  It is not a
claim that these mechanisms constitute biological intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Synapse:
    """A research relation with an explicit strength."""

    source: str
    target: str
    weight: float


@dataclass(frozen=True)
class LIFState:
    """Minimal leaky integrate-and-fire state for one node."""

    potential: float = 0.0
    spiked: bool = False


def lif_step(
    state: LIFState,
    input_current: float,
    *,
    leak: float = 0.2,
    threshold: float = 1.0,
) -> LIFState:
    """Advance one local activity step without a global controller."""
    potential = state.potential * (1.0 - leak) + input_current
    if potential >= threshold:
        return LIFState(potential=0.0, spiked=True)
    return LIFState(potential=potential, spiked=False)


def propagate(
    states: Mapping[str, LIFState],
    relations: Iterable[Synapse],
) -> dict[str, float]:
    """Compute local recurrent input from the current relation structure."""
    inputs = {node: 0.0 for node in states}
    for relation in relations:
        if relation.source in states and relation.target in inputs:
            if states[relation.source].spiked:
                inputs[relation.target] += relation.weight
    return inputs


def plasticity_step(
    relations: Iterable[Synapse],
    states: Mapping[str, LIFState],
    *,
    reinforce: float = 0.05,
    weaken: float = 0.02,
    extinction: float = 0.0,
) -> tuple[Synapse, ...]:
    """Apply local activity-dependent plasticity.

    A relation is strengthened when both endpoints are active, weakened when
    the source is active while the target is inactive, and removed when its
    resulting strength is at or below ``extinction``.  No external ranking or
    global selector is used.
    """
    updated: list[Synapse] = []
    for relation in relations:
        source = states.get(relation.source, LIFState())
        target = states.get(relation.target, LIFState())
        weight = relation.weight
        if source.spiked and target.spiked:
            weight += reinforce
        elif source.spiked and not target.spiked:
            weight -= weaken
        if weight > extinction:
            updated.append(Synapse(relation.source, relation.target, weight))
    return tuple(updated)


def structural_decay(relations: Iterable[Synapse], rate: float = 0.01) -> tuple[Synapse, ...]:
    """Apply continuous local decay; weak relations disappear."""
    factor = exp(-max(0.0, rate))
    return tuple(
        Synapse(r.source, r.target, r.weight * factor)
        for r in relations
        if r.weight * factor > 0.0
    )
