from __future__ import annotations

import json
from types import MappingProxyType
from typing import Any

from .agency_context import AgencyContext, AgencyIdentity
from .core_chat import CoreChat


def create_chat(subject: str = "anonymous") -> CoreChat:
    """Create a minimal chat session for the core API boundary."""
    context = AgencyContext(
        identity=AgencyIdentity(
            provider="core-api",
            subject=subject,
            authenticated=True,
        ),
        epoch=0,
        generation=0,
        height=0,
        expires_at=2**63 - 1,
    )
    return CoreChat(context)


def handle_chat(payload: dict[str, Any], chat: CoreChat) -> dict[str, Any]:
    """Handle one JSON-compatible chat request through the real CoreChat."""
    message = str(payload.get("message", ""))
    return chat.send(message)


def _json_safe(value: Any) -> Any:
    """Convert immutable core containers into ordinary JSON-compatible values."""
    if isinstance(value, MappingProxyType):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return [_json_safe(v) for v in value]
    return value


def dumps_response(result: dict[str, Any]) -> str:
    """Serialize a core chat result for an HTTP response."""
    return json.dumps(_json_safe(result), ensure_ascii=False)
