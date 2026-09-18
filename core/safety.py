"""Fail-closed autonomous operation safety contracts."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyGate:
    authority_gain: int = 0
    hard_stop: bool = False
    silence: bool = False
    max_operations: int = 20

    def allows(self, requested_operations: int) -> bool:
        if self.authority_gain != 0:
            return False
        if self.hard_stop or self.silence:
            return False
        if requested_operations < 0 or requested_operations > self.max_operations:
            return False
        return True

    def require(self, requested_operations: int) -> None:
        if not self.allows(requested_operations):
            raise PermissionError("autonomous operation blocked by safety gate")
