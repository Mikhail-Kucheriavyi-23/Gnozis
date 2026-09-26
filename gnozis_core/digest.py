"""Deterministic state digest boundary."""

import hashlib
import json
from collections.abc import Mapping
from .model import State


def _canonical(value):
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, tuple):
        return [_canonical(v) for v in value]
    if isinstance(value, frozenset):
        return sorted((_canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True, ensure_ascii=False))
    return value


def state_digest(state: State) -> str:
    payload = json.dumps(
        {"state_id": state.state_id, "version": state.version, "value": _canonical(state.value)},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
