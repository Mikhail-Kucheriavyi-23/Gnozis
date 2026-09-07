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


def dumps_response(result: dict[str, Any]) -> str:
    """Serialize a core chat result for an HTTP response."""
    return json.dumps(result, ensure_ascii=False)
