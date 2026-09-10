from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from core import Engine, State

from .agency_context import AgencyContext
from .core_evolution import engine_from_agency_context


ChatTransition = Callable[[State, AgencyContext], Mapping[str, Any]]


def default_chat_transition(
    state: State,
    context: AgencyContext,
) -> Mapping[str, Any]:
    """Minimal endogenous chat transition used until a richer cognition layer exists."""
    values = dict(state.values)
    message = str(values.pop("input_message", "")).strip()
    if not message:
        raise ValueError("state must contain an input message")

    history = list(values.get("history", []))
    history.append({"role": "user", "content": message})
    history.append(
        {
            "role": "core",
            "content": "Gnozis core received the message and evolved its state.",
        }
    )
    return {
        **values,
        "history": history,
        "turn": int(values.get("turn", 0)) + 1,
        "last_message": message,
        "agency_subject": context.identity.subject,
        "height": context.height,
    }


@dataclass
class CoreChat:
    """Small stateful chat adapter around the deterministic Gnozis core."""

    context: AgencyContext
    transition: ChatTransition = default_chat_transition
    state: State | None = None

    def __post_init__(self) -> None:
        if self.state is None:
            self.state = State(values={"turn": 0, "history": []})
        self.engine: Engine = engine_from_agency_context(
            self.context,
            lambda state, context: State(
                values=self.transition(state, context)
            ),
        )

    def send(self, message: str) -> dict[str, Any]:
        """Send one message through the core and return the new state snapshot."""
        message = str(message).strip()
        if not message:
            raise ValueError("message must not be empty")

        assert self.state is not None
        self.state = self.state.evolve(
            values={**self.state.values, "input_message": message}
        )
        self.state = self.engine.step(self.state)
        values = dict(self.state.values)
        history = list(values.get("history", []))
        response = next(
            (
                item["content"]
                for item in reversed(history)
                if item.get("role") == "core"
            ),
            "",
        )

        return {
            "response": response,
            "state": values,
        }
