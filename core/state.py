from   future   import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class State:
"""Immutable state of the GNOSIS/UROBOROS system."""

```
values: Mapping[str, Any] = field(default_factory=dict)

def evolve(self, *, values: Mapping[str, Any]) -> "State":
    """Create a new state without modifying the current state."""
    return State(values=dict(values))
```
