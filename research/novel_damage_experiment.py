"""Novel-damage experiment: tests adaptation to an unseen perturbation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .drosophila_principles import LIFState, Synapse
from .drosophila_damage_recovery import local_recovery_step, remove_relation


@dataclass(frozen=True)
class NovelDamageTrial:
    before: tuple[Synapse, ...]
    damaged: tuple[Synapse, ...]
    after: tuple[Synapse, ...]
    removed: tuple[str, str]


def run_novel_damage_trial(
    relations: tuple[Synapse, ...],
    states: Mapping[str, LIFState],
    *,
    source: str,
    target: str,
) -> NovelDamageTrial:
    """Apply a previously unseen relation damage and retain only structural state."""
    damaged = remove_relation(relations, source, target)
    after = local_recovery_step(damaged, states)
    return NovelDamageTrial(relations, damaged, after, (source, target))
