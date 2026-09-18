from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .engine import Engine
from .execution import CanonicalExecutor, Generator, Tester
from .relation import Relation
from .state import State
from .history import AppendOnlyHistory


def _unconfigured_transition(state: State) -> State:
    raise RuntimeError(
        "Uroboros has no transition configured; provide an Engine or use Uroboros.evolutionary()."
    )


@dataclass(frozen=True)
class Uroboros:
    """Recursive GNOSIS/UROBOROS computational core.

    The evolutionary constructor uses CanonicalExecutor as the production
    semantic path. State remains only the compatibility/adapter representation.
    """

    state: State = field(default_factory=State)
    engine: Engine = field(default_factory=lambda: Engine(transition=_unconfigured_transition))
    executor: CanonicalExecutor | None = None
    generate: Generator | None = None
    test: Tester | None = None

    @classmethod
    def evolutionary(
        cls,
        *,
        generate: Generator,
        test: Tester,
        state: State | None = None,
        kernel_version: str = "gnozis-core",
        history: AppendOnlyHistory | None = None,
    ) -> "Uroboros":
        initial = state or State()
        initial.to_psi()
        return cls(
            state=initial,
            engine=Engine(transition=_unconfigured_transition),
            executor=CanonicalExecutor(
                history=history or AppendOnlyHistory(),
                kernel_version=kernel_version,
            ),
            generate=generate,
            test=test,
        )

    def step(self) -> "Uroboros":
        if self.executor is not None:
            if self.generate is None or self.test is None:
                raise RuntimeError("Canonical executor requires generate and test.")
            result = self.executor.evolve(
                self.state.to_psi(),
                self.generate,
                self.test,
            )
            return Uroboros(
                state=State.from_psi(result.psi),
                engine=self.engine,
                executor=self.executor,
                generate=self.generate,
                test=self.test,
            )
        return Uroboros(state=self.engine.step(self.state), engine=self.engine)

    def with_relations(self, relations: Iterable[Relation]) -> "Uroboros":
        new_relations = tuple(relations)
        if any(not isinstance(relation, Relation) for relation in new_relations):
            raise TypeError("relations must contain Relation instances.")
        values = dict(self.state.values)
        values["relations"] = new_relations
        return Uroboros(
            state=State(values=values),
            engine=self.engine,
            executor=self.executor,
            generate=self.generate,
            test=self.test,
        )
