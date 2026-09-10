from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlparse

from .observation import Observation


@dataclass(frozen=True)
class WebObservationSource:
    """Read-only web adapter. Network data enters Ψ only as an Observation."""

    user_agent: str = "Gnozis-Observation/1.0"
    timeout: float = 15.0

    def fetch(self, url: str) -> Observation:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("url must be an absolute http(s) URL")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")

        request = Request(url, headers={"User-Agent": self.user_agent})
        with urlopen(request, timeout=self.timeout) as response:
            raw = response.read()
            content_type = response.headers.get_content_type()
            payload = json.loads(raw) if content_type == "application/json" else raw.decode("utf-8", errors="replace")
            status = getattr(response, "status", None)

        return Observation(
            source="web",
            payload=payload,
            observed_at=datetime.now(timezone.utc),
            provenance={"url": url, "content_type": content_type, "status": status},
        )
