from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .relation import Relation
from .state import Psi


class JsonlPsiMemory:
    """Append-only durable journal for proven Ψ states.

    A record is committed only after it can be reconstructed as a valid Psi.
    Invalid/truncated trailing records are ignored during recovery; earlier
    valid records remain usable. This adapter never mutates a Psi instance.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _encode(value: Any) -> Any:
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        if isinstance(value, list):
            return [JsonlPsiMemory._encode(v) for v in value]
        if isinstance(value, tuple):
            return [JsonlPsiMemory._encode(v) for v in value]
        if isinstance(value, dict):
            return {str(k): JsonlPsiMemory._encode(v) for k, v in value.items()}
        raise TypeError(f"unsupported Ψ value for durable storage: {type(value).__name__}")

    @classmethod
    def _record(cls, psi: Psi) -> dict[str, Any]:
        return {
            "x": cls._encode(psi.x),
            "relations": [
                {
                    "source": cls._encode(r.source),
                    "target": cls._encode(r.target),
                    "relation_type": r.relation_type,
                }
                for r in psi.relations
            ],
        }

    @staticmethod
    def _decode(record: dict[str, Any]) -> Psi:
        relations = tuple(
            Relation(r["source"], r["target"], r["relation_type"])
            for r in record["relations"]
        )
        return Psi(record["x"], relations)

    def save(self, psi: Psi) -> None:
        if not isinstance(psi, Psi):
            raise TypeError("psi must be a Psi instance")
        record = self._record(psi)
        # Validate before writing: an un-reconstructable state is never durable.
        self._decode(record)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            handle.flush()

    def load_latest(self) -> Psi | None:
        if not self.path.exists():
            return None
        latest: Psi | None = None
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                    if not isinstance(record, dict):
                        continue
                    candidate = self._decode(record)
                except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                    continue
                latest = candidate
        return latest
