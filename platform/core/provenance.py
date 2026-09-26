"""Minimal provenance record boundary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProvenanceRecord:
    operation_id: str
    actor_id: str
    input_state_id: str
    output_state_id: str | None
    operation: str
