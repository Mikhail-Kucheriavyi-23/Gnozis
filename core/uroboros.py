from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .evolution import Generator, Tester, evolutionary_psi_transition
from .relation import Relation
from .state import State


def _unconfigured_transition(state: State) -> State:
    """Prevent an unconfigured core from silently performing identity evolution."""
    raise RuntimeError(
        "Uroboros has no transition configured; provide an Engine or use Uroboros.evolutionary()."
    )


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core."""

    state: State = field(default_factory=State)
    engine: Engine = field(default_factory=lambda: Engine(transition=_unconfigured_transition))

    @classmethod
    def evolutionary(
        cls,
        *,
        generate: Generator,
        test: Tester,
        state: State | None = None,
    ) -> "Uroboros":
        """Create a core whose fundamental transition is Psi -> Psi."""
        initial = state or State()
        # Fail early if the supplied State cannot represent the fundamental Ψ=(X,R).
        initial.to_psi()
        return cls(
            state=initial,
            engine=Engine(transition=evolutionary_psi_transition(generate=generate, test=test)),
        )

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step."""
        return Uroboros(state=self.engine.step(self.state), engine=self.engine)

    def with_relations(self, relations: Iterable[Relation]) -> "Uroboros":
        """Return a new core with the same X and a replaced immutable relation set R."""
        new_relations = tuple(relations)
        values = dict(self.state.values)
        values["relations"] = new_relations
        return Uroboros(state=State(values=values), engine=self.engine)
