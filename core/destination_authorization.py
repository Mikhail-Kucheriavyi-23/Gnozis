"""Destination-scoped authorization for proposed outputs."""
from __future__ import annotations

from dataclasses import dataclass

from .information_contract import ValueClass
from .value_pipeline import OutputProposal


@dataclass(frozen=True)
class DestinationAuthorization:
    destination: str
    allowed_value_classes: frozenset[ValueClass]
    purpose: str

    def allows(self, proposal: OutputProposal) -> bool:
        return (
            proposal.destination == self.destination
            and proposal.value_class in self.allowed_value_classes
        )

    def require_allowed(self, proposal: OutputProposal) -> None:
        if not self.allows(proposal):
            raise PermissionError(
                "output destination is not authorized for this value class"
            )
