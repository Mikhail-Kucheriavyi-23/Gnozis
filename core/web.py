from __future__ import annotations

import ipaddress
import json
import socket
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.parse import urlparse

from .observation import Observation


class _NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(req.full_url, code, "redirects are disabled", headers, None)


def _host_is_public(host: str) -> bool:
    if not host or host.lower() == "localhost":
        return False
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(host, None)}
    except socket.gaierror as exc:
        raise ValueError("web host could not be resolved") from exc
    for address in addresses:
        if not ipaddress.ip_address(address).is_global:
            return False
    return True


@dataclass(frozen=True)
class WebObservationSource:
    """Read-only web adapter. Network data enters Ψ only as an Observation."""

    user_agent: str = "Gnozis-Observation/1.0"
    timeout: float = 15.0

    def fetch(self, url: str) -> Observation:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("url must be an absolute http(s) URL")
        if parsed.username or parsed.password:
            raise ValueError("URL credentials are not allowed")
        if not _host_is_public(parsed.hostname or ""):
            raise ValueError("web adapter refuses non-public destinations")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")

        request = Request(url, headers={"User-Agent": self.user_agent})
        opener = build_opener(_NoRedirectHandler())
        with opener.open(request, timeout=self.timeout) as response:
            raw = response.read()
            content_type = response.headers.get_content_type()
            payload = (
                json.loads(raw)
                if content_type == "application/json"
                else raw.decode("utf-8", errors="replace")
            )
            status = getattr(response, "status", None)

        return Observation(
            source="web",
            payload=payload,
            observed_at=datetime.now(timezone.utc),
            provenance={"url": url, "content_type": content_type, "status": status},
        )
