"""Minimal endogenous viability metrics for Ψ research experiments.

Viability is structural: active nodes must remain connected by the current
relation graph. This is a diagnostic, not an external optimizer or reward.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable, Mapping

from .drosophila_principles import LIFState, Synapse


def active_nodes(states: Mapping[str, LIFState]) -> frozenset[str]:
    return frozenset(node for node, state in states.items() if state.spiked)


def viability(states: Mapping[str, LIFState], relations: Iterable[Synapse]) -> float:
    """Return a structural viability score in [0, 1].

    Score is the fraction of active nodes reachable from one active node using
    positive-weight relations. Empty activity is non-viable (0.0).
    """
    active = active_nodes(states)
    if not active:
        return 0.0
    adjacency: dict[str, set[str]] = {node: set() for node in active}
    for relation in relations:
        if relation.weight > 0 and relation.source in active and relation.target in active:
            adjacency[relation.source].add(relation.target)
            adjacency[relation.target].add(relation.source)
    start = next(iter(active))
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) / len(active)
