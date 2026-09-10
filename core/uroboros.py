from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .evolution import Generator, Tester, evolutionary_transition
from .memory import PsiMemory
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core with optional Ψ recovery."""

    state: State = field(default_factory=State)
    engine: Engine = field(default_factory=lambda: Engine(transition=lambda state: state))
    memory: PsiMemory | None = None

    @classmethod
    def evolutionary(
        cls,
        *,
        generate: Generator,
        test: Tester,
        state: State | None = None,
        memory: PsiMemory | None = None,
    ) -> "Uroboros":
        """Create a core whose endogenous transition is Generate → Test → Select."""
        return cls(
            state=state or State(),
            engine=Engine(transition=evolutionary_transition(generate=generate, test=test)),
            memory=memory,
        )

    @classmethod
    def recover(cls, *, engine: Engine, memory: PsiMemory) -> "Uroboros":
        """Recover the latest persisted fundamental Ψ into the State wrapper."""
        psi = memory.load_latest()
        if psi is None:
            raise RuntimeError("persistent memory contains no valid Ψ")
        return cls(state=State.from_psi(psi), engine=engine, memory=memory)

    def step(self) -> "Uroboros":
        """Perform one endogenous evolution step and persist the resulting Ψ."""
        next_state = self.engine.step(self.state)
        if self.memory is not None:
            self.memory.save(next_state.to_psi())
        return Uroboros(state=next_state, engine=self.engine, memory=self.memory)

    def with_relations(self, relations: Iterable[Relation]) -> "Uroboros":
        """Return a new core with the same X and a replaced immutable relation set R."""
        new_relations = tuple(relations)
        values = dict(self.state.values)
        values["relations"] = new_relations
        return Uroboros(state=State(values=values), engine=self.engine, memory=self.memory)
