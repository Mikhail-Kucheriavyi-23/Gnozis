"""Certified snapshots: cache/observation only, never semantic source of truth."""
from __future__ import annotations

from dataclasses import dataclass

from .state import Psi


@dataclass(frozen=True)
class SnapshotCertificate:
    history_head: str
    state_hash: str
    kernel_version: str


@dataclass(frozen=True)
class Snapshot:
    state: Psi
    certificate: SnapshotCertificate

    def is_cache_of(self, history_head: str, state_hash: str, kernel_version: str) -> bool:
        return (
            self.certificate.history_head == history_head
            and self.certificate.state_hash == state_hash
            and self.certificate.kernel_version == kernel_version
        )
