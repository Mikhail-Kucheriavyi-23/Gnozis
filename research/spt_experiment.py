"""SPT-MVP: minimal structural persistence transfer experiment.

This module is intentionally isolated from the Ψ-Core. It records the
experimental protocol; it does not claim to prove SPT by itself.

Protocol:
    baseline -> training -> capture structural state -> clear episodic memory
    -> novel evaluation.

The MVP deliberately excludes random controls, reversibility, and statistics.
Those are subsequent gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class SPTResult:
    """Immutable record of one SPT-MVP run."""

    seed: int
    training_hash: str
    novel_input_hash: str
    structure_before: tuple[Any, ...]
    structure_after: tuple[Any, ...]
    episodic_memory_after_clear: tuple[Any, ...]
    score_before: float
    score_after: float

    @property
    def structure_changed(self) -> bool:
        return self.structure_before != self.structure_after

    @property
    def transfer_delta(self) -> float:
        return self.score_after - self.score_before


@dataclass
class SPTExperiment:
    """Minimal orchestration layer for an SPT-MVP run.

    Callbacks keep the research experiment independent from Ψ-Core internals.
    """

    train: Callable[[Mapping[str, Any]], None]
    snapshot_structure: Callable[[], tuple[Any, ...]]
    clear_episodic_memory: Callable[[], None]
    episodic_memory: Callable[[], tuple[Any, ...]]
    evaluate: Callable[[Mapping[str, Any]], float]
    seed: int = 0
    training_hash: str = ""
    novel_input_hash: str = ""

    def run(
        self,
        training_input: Mapping[str, Any],
        novel_input: Mapping[str, Any],
    ) -> SPTResult:
        structure_before = tuple(self.snapshot_structure())
        score_before = float(self.evaluate(novel_input))

        self.train(training_input)
        structure_after = tuple(self.snapshot_structure())

        self.clear_episodic_memory()
        memory_after_clear = tuple(self.episodic_memory())

        score_after = float(self.evaluate(novel_input))

        return SPTResult(
            seed=self.seed,
            training_hash=self.training_hash,
            novel_input_hash=self.novel_input_hash,
            structure_before=structure_before,
            structure_after=structure_after,
            episodic_memory_after_clear=memory_after_clear,
            score_before=score_before,
            score_after=score_after,
        )
