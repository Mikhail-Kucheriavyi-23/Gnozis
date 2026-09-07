from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any, Mapping

from core.state import State
from core.uroboros import Uroboros


@dataclass
class GnosisTerminal:
    """Small stdin/stdout bridge for interactive GNOSIS/UROBOROS sessions.

    Each input line is one JSON command and each output line is one JSON result.
    The bridge deliberately keeps transport concerns outside the Ψ-Core.
    """

    core: Uroboros = field(default_factory=Uroboros)
    evolution_steps: int = 0
    received_messages: int = 0
    history: list[dict[str, Any]] = field(default_factory=list)

    def status(self) -> dict[str, Any]:
        """Return observable runtime state without inventing intelligence metrics."""
        return {
            "status": "ready",
            "architecture": "State -> Relation -> Engine -> UROBOROS",
            "state": dict(self.core.state.values),
            "evolution_steps": self.evolution_steps,
            "received_messages": self.received_messages,
            "history_length": len(self.history),
            "capabilities": ["status", "inject", "step", "evolution"],
        }

    def inject(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Store an external message in state and record the event."""
        values = dict(self.core.state.values)
        values["last_input"] = dict(payload)
        values["input_count"] = self.received_messages + 1
        self.core = Uroboros(state=self.core.state.evolve(values=values), engine=self.core.engine)
        self.received_messages += 1
        event = {"type": "inject", "payload": dict(payload)}
        self.history.append(event)
        return {"status": "accepted", "state": dict(self.core.state.values)}

    def step(self) -> dict[str, Any]:
        """Execute one endogenous core step and record it."""
        self.core = self.core.step()
        self.evolution_steps += 1
        event = {"type": "step", "step": self.evolution_steps}
        self.history.append(event)
        return {"status": "stepped", "evolution_steps": self.evolution_steps, "state": dict(self.core.state.values)}

    def evolution(self) -> dict[str, Any]:
        """Return measured evolution counters and event history."""
        return {
            "evolution_steps": self.evolution_steps,
            "received_messages": self.received_messages,
            "history_length": len(self.history),
            "history": list(self.history),
        }

    def dispatch(self, command: Mapping[str, Any]) -> dict[str, Any]:
        """Dispatch one JSON command."""
        action = command.get("action", "status")
        if action == "status":
            return self.status()
        if action == "inject":
            payload = command.get("data", {})
            if not isinstance(payload, Mapping):
                raise TypeError("inject.data must be a JSON object")
            return self.inject(payload)
        if action == "step":
            return self.step()
        if action == "evolution":
            return self.evolution()
        raise ValueError(f"unknown action: {action}")


def main() -> None:
    terminal = GnosisTerminal()
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            command = json.loads(line)
            if not isinstance(command, Mapping):
                raise TypeError("command must be a JSON object")
            result = terminal.dispatch(command)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
        except Exception as exc:  # Keep the transport alive after malformed input.
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
