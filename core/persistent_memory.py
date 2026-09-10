from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

from .observation import Observation


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return [_jsonable(v) for v in value]
    return value


class JsonlObservationStore:
    """Durable append-only observation memory with no dependency on Engine state."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def remember(self, item: Observation) -> None:
        if not isinstance(item, Observation):
            raise TypeError("memory accepts Observation instances only")
        record = {
            "source": item.source,
            "payload": _jsonable(item.payload),
            "observed_at": item.observed_at.isoformat(),
            "provenance": _jsonable(item.provenance),
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")

    def recall(self, *, limit: int = 100) -> tuple[Observation, ...]:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            raise TypeError("limit must be a non-negative int")
        if limit == 0 or not self.path.exists():
            return ()
        with self.path.open("r", encoding="utf-8") as handle:
            records = [json.loads(line) for line in handle if line.strip()]
        return tuple(
            Observation(
                source=record["source"],
                payload=record["payload"],
                observed_at=datetime.fromisoformat(record["observed_at"]),
                provenance=record.get("provenance", {}),
            )
            for record in records[-limit:]
        )
