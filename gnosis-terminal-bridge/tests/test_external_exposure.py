from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from src.chat_server import GnozisChatHandler
from src.internet_port import MAX_BODY_BYTES


def _server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), GnozisChatHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def test_oversized_body_rejected():
    server = _server()
    try:
        url = f"http://127.0.0.1:{server.server_port}/v1/handshake"
        payload = json.dumps({
            "protocol": "gnozis-port/1",
            "client_id": "x",
            "provenance": {"source": "x"},
            "padding": "x" * MAX_BODY_BYTES,
        }).encode()
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            urllib.request.urlopen(req, timeout=2)
            assert False, "expected HTTP 413"
        except urllib.error.HTTPError as exc:
            assert exc.code == 413
    finally:
        server.shutdown(); server.server_close()


def test_unknown_route_is_not_exposed():
    server = _server()
    try:
        url = f"http://127.0.0.1:{server.server_port}/internal"
        req = urllib.request.Request(url, method="GET")
        try:
            urllib.request.urlopen(req, timeout=2)
            assert False, "expected HTTP 404"
        except urllib.error.HTTPError as exc:
            assert exc.code == 404
    finally:
        server.shutdown(); server.server_close()
