from __future__ import annotations

from typing import Protocol, Sequence

from .observation import Observation
from .state import Psi


class Memory(Protocol):
    """Explicit memory boundary used by adapters, not by hidden Engine state."""

    def remember(self, item: Observation) -> None: ...

    def recall(self, *, limit: int = 100) -> Sequence[Observation]: ...


class InMemoryStore:
    """Small deterministic append-only memory implementation for local use/tests."""

    def __init__(self) -> None:
        self._items: list[Observation] = []

    def remember(self, item: Observation) -> None:
        if not isinstance(item, Observation):
            raise TypeError("memory accepts Observation instances only")
        self._items.append(item)

    def recall(self, *, limit: int = 100) -> tuple[Observation, ...]:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            raise TypeError("limit must be a non-negative int")
        return tuple(self._items[-limit:]) if limit else ()

    def snapshot(self) -> tuple[Observation, ...]:
        return tuple(self._items)


class PsiMemory(Protocol):
    """Optional persistence boundary for Ψ states."""

    def save(self, psi: Psi) -> None: ...

    def load_latest(self) -> Psi | None: ...
