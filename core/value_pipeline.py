"""Minimal runtime for classifying value and proposing an output."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .information_contract import Information, ValueClass


class OutputStatus(str, Enum):
    PROPOSED = "PROPOSED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class OutputProposal:
    information_id: str
    value_class: ValueClass
    destination: str
    content_reference: str
    provenance_ref: str
    status: OutputStatus = OutputStatus.PROPOSED


def classify_value(information: Information, value_class: ValueClass) -> ValueClass:
    information.require_authorized()
    if not isinstance(value_class, ValueClass):
        raise TypeError("value_class must be ValueClass.")
    return value_class


def propose_output(
    information: Information,
    *,
    value_class: ValueClass,
    destination: str,
    content_reference: str | None = None,
) -> OutputProposal:
    information.require_authorized()
    if not destination.strip():
        raise ValueError("destination is required")
    classified = classify_value(information, value_class)
    return OutputProposal(
        information_id=information.information_id,
        value_class=classified,
        destination=destination,
        content_reference=content_reference or information.content_reference,
        provenance_ref=information.provenance_ref,
    )
