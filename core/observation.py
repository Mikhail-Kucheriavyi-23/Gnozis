from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .state import _freeze


@dataclass(frozen=True)
class Observation:
    """Immutable external observation; never applied to Ψ automatically."""

    source: str
    payload: Any
    observed_at: datetime
    provenance: Mapping[str, Any] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("Observation.source must be a non-empty string")
        if self.observed_at.tzinfo is None:
            raise ValueError("Observation.observed_at must be timezone-aware")
        object.__setattr__(self, "observed_at", self.observed_at.astimezone(timezone.utc))
        object.__setattr__(self, "payload", _freeze(self.payload))
        object.__setattr__(self, "provenance", _freeze(dict(self.provenance)))
