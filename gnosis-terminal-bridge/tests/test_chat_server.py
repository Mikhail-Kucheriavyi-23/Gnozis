from __future__ import annotations

import json
from http.client import HTTPConnection
from threading import Thread

from src.chat_server import GnozisChatHandler, ThreadingHTTPServer


def test_chat_server_health_and_chat_roundtrip() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), GnozisChatHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=2)
        connection.request("GET", "/health")
        response = connection.getresponse()
        assert response.status == 200
        assert json.loads(response.read()) == {"status": "online", "core": "ready"}

        connection.request(
            "POST",
            "/chat",
            body=json.dumps({"message": "hello"}),
            headers={"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        payload = json.loads(response.read())
        assert response.status == 200
        assert payload["state"]["turn"] >= 1
        assert payload["state"]["last_message"] == "hello"
        assert payload["response"]
        connection.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
