"""Repeated-damage experiment for structural-memory hypothesis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_principles import LIFState, Synapse
from .drosophila_damage_recovery import local_recovery_step, remove_relation


@dataclass(frozen=True)
class Trial:
    relations_before: tuple[Synapse, ...]
    damaged: tuple[Synapse, ...]
    relations_after: tuple[Synapse, ...]


def repeated_damage(
    relations: tuple[Synapse, ...],
    states: Mapping[str, LIFState],
    source: str,
    target: str,
    repeats: int = 2,
) -> tuple[Trial, ...]:
    """Repeat identical damage while retaining only structural state between trials."""
    current = relations
    trials: list[Trial] = []
    for _ in range(max(0, repeats)):
        damaged = remove_relation(current, source, target)
        after = local_recovery_step(damaged, states)
        trials.append(Trial(current, damaged, after))
        current = after
    return tuple(trials)
