from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .engine import Engine
from .evolution import Generator, Tester, evolutionary_transition
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core."""

    state: State
    engine: Engine

    @classmethod
    def evolutionary(
        cls,
        *,
        generate: Generator,
        test: Tester,
        state: State | None = None,
    ) -> "Uroboros":
        """Create a core whose transition is Generate -> Test -> Select."""
        return cls(
            state=state if state is not None else State(),
            engine=Engine(
                transition=evolutionary_transition(generate=generate, test=test)
            ),
        )

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step."""
        return Uroboros(state=self.engine.step(self.state), engine=self.engine)

    def with_relations(self, relations: Iterable[Relation]) -> "Uroboros":
        """Return a new core with the same X and a replaced immutable R."""
        values = dict(self.state.values)
        values["relations"] = tuple(relations)
        return Uroboros(state=State(values=values), engine=self.engine)
