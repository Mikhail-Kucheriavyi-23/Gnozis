"""Runtime information and authorization contracts for Market Information Loop v1."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class AuthorizationStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    ALLOWED = "ALLOWED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class ValueClass(str, Enum):
    PUBLIC = "PUBLIC"
    COMMERCIAL = "COMMERCIAL"
    PERSONAL = "PERSONAL"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Authorization:
    source: str
    purpose: str
    operation: str
    destination: str
    status: AuthorizationStatus = AuthorizationStatus.UNKNOWN
    validity_ref: str | None = None

    def allows(self) -> bool:
        return self.status is AuthorizationStatus.ALLOWED

    def require_allowed(self) -> None:
        if not self.allows():
            raise PermissionError(
                f"information is not authorized: status={self.status.value}"
            )


@dataclass(frozen=True)
class Information:
    information_id: str
    source: str
    content_reference: str
    provenance_ref: str
    authorization: Authorization
    value_class: ValueClass = ValueClass.UNKNOWN
    payload: Any = None

    def require_authorized(self) -> None:
        self.authorization.require_allowed()
