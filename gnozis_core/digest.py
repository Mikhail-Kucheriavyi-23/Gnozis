"""Deterministic state digest boundary."""

import hashlib
import json
from .model import State


def state_digest(state: State) -> str:
    payload = json.dumps(
        {"state_id": state.state_id, "version": state.version, "value": state.value},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
