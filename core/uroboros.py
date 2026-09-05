from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .engine import Engine
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core."""

    state: State
    engine: Engine

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step."""
        next_state = self.engine.step(
            state=self.state,
            relations=(),
        )
        return Uroboros(
            state=next_state,
            engine=self.engine,
        )

    def with_relations(
        self,
        relations: Iterable[Relation],
    ) -> "Uroboros":
        """Return a core instance configured with the supplied relations."""
        next_state = self.engine.step(
            state=self.state,
            relations=relations,
        )
        return Uroboros(
            state=next_state,
            engine=self.engine,
        )
