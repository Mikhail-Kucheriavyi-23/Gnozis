from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .chat_api import create_chat, handle_chat


class GnozisChatHandler(BaseHTTPRequestHandler):
    """Minimal stdlib HTTP adapter for the Gnozis core chat."""

    chat = create_chat()

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._json(204, {})

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"status": "online", "core": "ready"})
            return
        self._json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path != "/chat":
            self._json(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(payload, dict):
                raise ValueError("JSON body must be an object")
            result = handle_chat(payload, self.chat)
        except (json.JSONDecodeError, ValueError) as exc:
            self._json(400, {"error": str(exc)})
            return
        except Exception as exc:
            self._json(500, {"error": str(exc)})
            return

        self._json(200, result)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "0.0.0.0", port: int = 8788) -> None:
    server = ThreadingHTTPServer((host, port), GnozisChatHandler)
    print(f"Gnozis Core API listening on http://{host}:{port}", flush=True)
    print("POST /chat   GET /health", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
