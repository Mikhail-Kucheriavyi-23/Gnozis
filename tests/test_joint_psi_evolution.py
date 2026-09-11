"""Verify joint endogenous evolution of X and R in a single transition."""

from core import State
from core.evolution import evolutionary_transition


def test_x_and_r_can_evolve_together():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    candidate = State(
        values={
            "x": ("a", "b"),
            "relations": (("b", "c"),),
        }
    )

    result = evolutionary_transition(lambda _state: (candidate,), lambda _s: True)(initial)

    assert result.values["x"] != initial.values["x"]
    assert result.to_psi().relations != initial.to_psi().relations
    assert result == candidate


def test_test_controls_joint_psi_change():
    initial = State(values={"x": ("a",), "relations": (("a", "b"),)})
    valid = State(values={"x": ("a", "b"), "relations": (("b", "c"),)})
    invalid = State(values={"x": ("a", "b"), "relations": ()})

    def test(candidate):
        psi = candidate.to_psi()
        return psi.relations == (("b", "c"),)

    result = evolutionary_transition(lambda _state: (invalid, valid), test)(initial)

    assert result == valid
    assert result.values["x"] == ("a", "b")
    assert result.to_psi().relations == (("b", "c"),)
