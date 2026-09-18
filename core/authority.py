"""Explicit authority boundary: external evidence is never execution authority."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Evidence:
    source: str
    payload: Any


@dataclass(frozen=True)
class AuthorityDecision:
    admitted: bool
    reason: str


def foreign_evidence_is_non_authoritative(evidence: Evidence) -> AuthorityDecision:
    return AuthorityDecision(
        admitted=False,
        reason="foreign evidence may inform proof; it cannot authorize execution",
    )
