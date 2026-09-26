"""Admission gate for authorized information before task processing."""
from __future__ import annotations

from .information_contract import Information


def admit_information(information: Information) -> Information:
    """Fail closed before information enters task processing."""
    information.require_authorized()
    return information
