from   future   import annotations

from .engine import Engine
from .state import State

class Uroboros:
"""Recursive runtime for the GNOSIS/UROBOROS core."""


def __init__(
    self,
    initial_state: State,
    rules=None,
):
    self.state = initial_state
    self.engine = Engine(rules)

def step(self) -> State:
    """Perform one endogenous evolution step."""
    self.state = self.engine.step(self.state)
    return self.state

def run(self, steps: int) -> State:
    """Run the recursive evolution cycle."""
    if steps < 0:
        raise ValueError("steps must be non-negative")

    for _ in range(steps):
        self.step()

    return self.state

