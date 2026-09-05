from **future** import annotations

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Relation:
"""
Minimal relation between two elements of a system.
"""

```
source: Any
target: Any
value: Any = None
```
