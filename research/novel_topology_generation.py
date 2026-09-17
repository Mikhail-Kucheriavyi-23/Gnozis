"""Bounded endogenous topology-generation experiment for Ψ=(X,R).

This is deliberately a research mechanism, not part of the canonical core.
New relations can arise only from already-active nodes and a local co-activity
rule; no target topology, repair plan, selector, reward model, or global
optimizer is supplied.
"""

from __future__ import annotations

from typing import Mapping

from .drosophila_principles import LIFState, Synapse


def generate_local_relations(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
    *,
    creation_weight: float = 0.05,
) -> tuple[Synapse, ...]:
    """Create previously absent directed relations between co-active nodes."""
    active = tuple(sorted(node for node, state in states.items() if state.spiked))
    existing = {(r.source, r.target) for r in relations}
    generated = list(relations)
    for source in active:
        for target in active:
            if source == target or (source, target) in existing:
                continue
            generated.append(Synapse(source, target, creation_weight))
    return tuple(generated)


def topology_step(
    states: Mapping[str, LIFState],
    relations: tuple[Synapse, ...],
) -> tuple[Synapse, ...]:
    """One bounded endogenous topology-generation step."""
    return generate_local_relations(states, relations)
