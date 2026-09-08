from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .evolution import Generator, Selector, Tester, evolutionary_transition
from .relation import Relation
from .state import State


@dataclass(frozen=True)
class Uroboros:
    """Recursive Ψ core carrying state, relations and endogenous evolution."""

    state: State = field(default_factory=State)
    engine: Engine = field(default_factory=lambda: Engine(transition=lambda state: state))
    relations: tuple[Relation, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        normalized_relations = tuple(self.relations)
        if self.state.relations and normalized_relations and self.state.relations != normalized_relations:
            raise ValueError("Uroboros relations must match State relations")
        if not normalized_relations and self.state.relations:
            normalized_relations = self.state.relations
        elif normalized_relations and not self.state.relations:
            object.__setattr__(self, "state", self.state.evolve(values=self.state.values, relations=normalized_relations))
        object.__setattr__(self, "relations", normalized_relations)

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
        relations_tuple = tuple(relations)
        initial_state = state if state is not None else State(relations=relations_tuple)
        if initial_state.relations and relations_tuple and initial_state.relations != relations_tuple:
            raise ValueError("Initial State relations must match Uroboros relations")
        return cls(
            state=initial_state,
            engine=Engine(transition=evolutionary_transition(generate, test, select)),
            relations=relations_tuple or initial_state.relations,
        )

    def step(self) -> "Uroboros":
        next_state = self.engine.step(self.state)
        if next_state.relations != self.relations:
            next_state = next_state.evolve(values=next_state.values, relations=self.relations)
        return Uroboros(state=next_state, engine=self.engine, relations=self.relations)

    def with_relations(self, relations: Iterable[Relation]) -> "Uroboros":
        relations_tuple = tuple(relations)
        return Uroboros(
            state=self.state.evolve(values=self.state.values, relations=relations_tuple),
            engine=self.engine,
            relations=relations_tuple,
        )
