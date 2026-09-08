from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .evolution import Generator, Selector, Tester, evolutionary_transition
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core."""

    state: State = field(default_factory=State)
    engine: Engine = field(
        default_factory=lambda: Engine(transition=lambda state: state)
    )

    def __post_init__(self) -> None:
        if not isinstance(self.state, State):
            raise TypeError("Uroboros.state must be a State instance.")
        if not isinstance(self.engine, Engine):
            raise TypeError("Uroboros.engine must be an Engine instance.")

    @classmethod
    def evolutionary(
        cls,
        *,
        generate: Generator,
        test: Tester,
        select: Selector,
        state: State | None = None,
    ) -> "Uroboros":
        """Create a core whose endogenous transition is Generate → Test → Select."""
        return cls(
            state=state if state is not None else State(),
            engine=Engine(
                transition=evolutionary_transition(
                    generate=generate,
                    test=test,
                    select=select,
                )
            ),
        )

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step and return a new core."""
        return Uroboros(
            state=self.engine.step(self.state),
            engine=self.engine,
        )

    def run(self, steps: int) -> "Uroboros":
        """Perform multiple endogenous evolution steps without external selection."""
        if steps < 0:
            raise ValueError("steps must be non-negative.")

        current = self
        for _ in range(steps):
            current = current.step()
        return current

    def with_relations(
        self,
        relations: Iterable[Relation],
    ) -> "Uroboros":
        """Return a new core whose State owns the supplied relations."""
        return Uroboros(
            state=self.state.evolve(relations=tuple(relations)),
            engine=self.engine,
        )
