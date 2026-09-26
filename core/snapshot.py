"""Certified snapshots: cache/observation only, never semantic source of truth."""
from __future__ import annotations

from dataclasses import dataclass

from .execution_contract import state_digest
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

    def is_valid_for_replay(
        self,
        replayed_state: Psi,
        *,
        history_head: str,
        kernel_version: str,
    ) -> bool:
        """Accept cache only when certificate and replay result agree."""
        if not isinstance(replayed_state, Psi):
            raise TypeError("replayed_state must be Psi.")
        actual_state_hash = state_digest(replayed_state)
        return self.is_cache_of(
            history_head,
            actual_state_hash,
            kernel_version,
        )

    def invalidate_if_stale(
        self,
        replayed_state: Psi,
        *,
        history_head: str,
        kernel_version: str,
    ) -> "Snapshot | None":
        """Return the snapshot only when it is still certified by replay."""
        if self.is_valid_for_replay(
            replayed_state,
            history_head=history_head,
            kernel_version=kernel_version,
        ):
            return self
        return None
