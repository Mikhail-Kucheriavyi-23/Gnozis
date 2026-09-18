"""Explicit compatibility-authority marker for the legacy State transition path."""

from __future__ import annotations

from .state import State


def is_canonical_authority(value: object) -> bool:
    """Legacy State values are never canonical semantic authority."""
    return False


def reject_as_canonical(value: object) -> State:
    if isinstance(value, State):
        raise TypeError("Legacy State is compatibility-only and cannot be canonical authority.")
    raise TypeError("Only legacy State compatibility values are classified here.")
