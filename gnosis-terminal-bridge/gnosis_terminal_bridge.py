"""Compatibility entry point for the terminal bridge.

The canonical implementation lives in ``src.gnosis_terminal_bridge``.
Keeping this module as a thin re-export prevents the legacy test/import path
from drifting away from the canonical implementation.
"""

from src.gnosis_terminal_bridge import Challenge, GnosisTerminalBridge, handle

__all__ = ["Challenge", "GnosisTerminalBridge", "handle"]


if __name__ == "__main__":
    import json
    import sys

    request = json.load(sys.stdin)
    response = handle(request)
    print(json.dumps(response, indent=2))
