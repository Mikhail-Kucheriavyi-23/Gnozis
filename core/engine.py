from **future** import annotations

from collections.abc import Callable

from .state import State

Rule = Callable[[State], State]

class Engine:
"""
Minimal endogenous evolution engine.

```
The engine repeatedly applies internally defined rules to the
current state.
"""

def __init__(self, rules: list[Rule] | None = None):
    self.rules = list(rules or [])

def add_rule(self, rule: Rule) -> None:
    self.rules.append(rule)

def step(self, state: State) -> State:
    """
    Perform one endogenous evolution step.
    """
    next_state = state

    for rule in self.rules:
        next_state = rule(next_state)

    return next_state

def run(self, state: State, steps: int) -> State:
    """
    Run the endogenous evolution cycle.
    """
    if steps < 0:
        raise ValueError("steps must be non-negative")

    current = state

    for _ in range(steps):
        current = self.step(current)

    return current
```
