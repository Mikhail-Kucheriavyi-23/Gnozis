"""Hard runtime boundary between compatibility State transitions and canonical Ψ state.

LegacyEngine may transform State for compatibility, but canonical semantic
commit must explicitly reject legacy-produced states.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .state import Psi, State


@dataclass(frozen=True)
class CanonicalPsiInput:
    psi: Psi


def canonicalize_psi(value: Any) -> CanonicalPsiInput:
    """Accept only an explicit Psi as canonical semantic input.

    A legacy State is intentionally not auto-coerced into canonical Ψ input.
    """
    if isinstance(value, CanonicalPsiInput):
        return value
    if isinstance(value, Psi):
        return CanonicalPsiInput(value)
    if isinstance(value, State):
        raise TypeError(
            "Legacy State cannot cross the canonical Ψ boundary implicitly."
        )
    raise TypeError("Canonical semantic input must be Psi.")


def commit_canonical(value: Any) -> Psi:
    """Return canonical Ψ only from an explicit canonical boundary object."""
    return canonicalize_psi(value).psi
