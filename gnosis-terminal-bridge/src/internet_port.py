from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import dataclass, field
from typing import Any

PROTOCOL = "gnozis-port/1"
MAX_BODY_BYTES = 64 * 1024
SESSION_TTL_SECONDS = 3600
ALLOWED_TYPES = {"observation", "hypothesis", "request", "candidate"}


@dataclass
class PortSession:
    session_id: str
    client_id: str
    protocol: str
    created_at: float
    expires_at: float
    seen_messages: set[str] = field(default_factory=set)


class PortError(ValueError):
    pass


class InternetPort:
    """Small, dependency-free protocol boundary around a Gnozis adapter.

    The port validates transport/session semantics. It does not become a
    selector for the Gnozis core. A caller supplies `handler`, which receives
    an already validated exchange and returns a result.
    """

    def __init__(self, handler):
        self.handler = handler
        self.sessions: dict[str, PortSession] = {}

    def handshake(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise PortError("handshake must be an object")
        if payload.get("protocol") != PROTOCOL:
            raise PortError("unsupported protocol")
        client_id = payload.get("client_id")
        provenance = payload.get("provenance")
        if not isinstance(client_id, str) or not client_id.strip():
            raise PortError("client_id required")
        if not isinstance(provenance, dict):
            raise PortError("provenance required")

        now = time.time()
        session_id = secrets.token_urlsafe(24)
        self.sessions[session_id] = PortSession(
            session_id=session_id,
            client_id=client_id,
            protocol=PROTOCOL,
            created_at=now,
            expires_at=now + SESSION_TTL_SECONDS,
        )
        return {
            "protocol": PROTOCOL,
            "status": "accepted",
            "session_id": session_id,
            "expires_at": self.sessions[session_id].expires_at,
        }

    def exchange(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise PortError("exchange must be an object")
        if payload.get("protocol") != PROTOCOL:
            raise PortError("unsupported protocol")

        session_id = payload.get("session_id")
        message_id = payload.get("message_id")
        message_type = payload.get("type")
        provenance = payload.get("provenance")

        if not isinstance(session_id, str) or not session_id:
            raise PortError("session_id required")
        if not isinstance(message_id, str) or not message_id:
            raise PortError("message_id required")
        if message_type not in ALLOWED_TYPES:
            raise PortError("unsupported message type")
        if not isinstance(provenance, dict):
            raise PortError("provenance required")

        session = self.sessions.get(session_id)
        if session is None:
            raise PortError("unknown session")
        if time.time() >= session.expires_at:
            del self.sessions[session_id]
            raise PortError("session expired")
        if message_id in session.seen_messages:
            raise PortError("replayed message_id")

        session.seen_messages.add(message_id)
        body = payload.get("payload")
        if not isinstance(body, dict):
            raise PortError("payload must be an object")

        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        envelope = {
            "protocol": PROTOCOL,
            "session_id": session_id,
            "message_id": message_id,
            "type": message_type,
            "payload": body,
            "provenance": provenance,
            "payload_sha256": payload_hash,
        }

        result = self.handler(envelope)
        if not isinstance(result, dict):
            raise PortError("handler must return an object")

        return {
            "protocol": PROTOCOL,
            "message_id": message_id,
            "status": "accepted",
            "reason": "",
            "result": result,
        }
