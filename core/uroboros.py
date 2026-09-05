from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core."""

    state: State = field(default_factory=State)
    engine: Engine = field(
        default_factory=lambda: Engine(
            transition=lambda state: state
        )
    )

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step."""
        next_state = self.engine.step(self.state)

        return Uroboros(
            state=next_state,
            engine=self.engine,
        )

    def with_relations(
        self,
        relations: Iterable[Relation],
    ) -> "Uroboros":
        """Return a core instance configured with the supplied relations."""
        _ = tuple(relations)

        return Uroboros(
            state=self.state,
            engine=self.engine,
        )
