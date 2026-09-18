from core.legacy_engine import LegacyEngine
from core.state import State


def test_legacy_engine_is_explicitly_noncanonical():
    state = State(values={"x": 0, "relations": ()})
    engine = LegacyEngine(lambda s: s.evolve(values={"x": 1, "relations": ()}))
    assert engine.step(state).values["x"] == 1
