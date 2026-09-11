from __future__ import annotations

import json
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


def _wire_value(value: Any) -> Any:
    """Convert immutable core containers into JSON-compatible wire values."""
    if isinstance(value, dict):
        return {str(key): _wire_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_wire_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "items"):
        return {str(key): _wire_value(item) for key, item in value.items()}
    return str(value)


def dumps_response(result: dict[str, Any]) -> str:
    """Serialize a core result at the external wire boundary only."""
    return json.dumps(_wire_value(result), ensure_ascii=False)
