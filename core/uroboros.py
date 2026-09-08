from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .evolution import Generator, Selector, Tester, evolutionary_transition
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core.

    Relations are part of the explicit core configuration. They are preserved
    across endogenous steps and are no longer silently discarded by
    ``with_relations``.
    """

    state: State = field(default_factory=State)
    engine: Engine = field(
        default_factory=lambda: Engine(
            transition=lambda state: state
        )
    )
    relations: tuple[Relation, ...] = field(default_factory=tuple)

    @classmethod
    def evolutionary(
        cls,
        *,
        generate: Generator,
        test: Tester,
        select: Selector,
        state: State | None = None,
        relations: Iterable[Relation] = (),
    ) -> "Uroboros":
        """Create a core with endogenous Generate → Test → Select evolution."""
        return cls(
            state=state if state is not None else State(),
            engine=Engine(
                transition=evolutionary_transition(
                    generate=generate,
                    test=test,
                    select=select,
                )
            ),
            relations=tuple(relations),
        )

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step while preserving relations."""
        next_state = self.engine.step(self.state)

        return Uroboros(
            state=next_state,
            engine=self.engine,
            relations=self.relations,
        )

    def with_relations(
        self,
        relations: Iterable[Relation],
    ) -> "Uroboros":
        """Return an immutable core instance with the supplied relations."""
        return Uroboros(
            state=self.state,
            engine=self.engine,
            relations=tuple(relations),
        )
