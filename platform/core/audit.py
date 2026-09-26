"""Minimal append-only audit boundary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditRecord:
    sequence: int
    operation_id: str
    event: str
    previous_digest: str
    record_digest: str


class AuditChain:
    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(self, operation_id: str, event: str, record_digest: str) -> AuditRecord:
        previous = self._records[-1].record_digest if self._records else "GENESIS"
        record = AuditRecord(len(self._records), operation_id, event, previous, record_digest)
        self._records.append(record)
        return record

    def records(self) -> tuple[AuditRecord, ...]:
        return tuple(self._records)
