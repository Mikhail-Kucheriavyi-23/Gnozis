"""Typed external operations; authorization never selects a state transition."""
from __future__ import annotations

from enum import Enum


class ExternalOperation(str, Enum):
    OBSERVE = "observe"
    REQUEST = "request"
    PROPOSE = "propose"
    CANDIDATE = "candidate"


def parse_external_operation(value: str) -> ExternalOperation:
    try:
        return ExternalOperation(value)
    except ValueError as exc:
        raise ValueError(f"unsupported external operation: {value!r}") from exc
