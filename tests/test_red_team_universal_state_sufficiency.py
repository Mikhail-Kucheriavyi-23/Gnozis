import pytest

from core.engine import Engine
from core.state import State


@pytest.mark.xfail(reason="Current State->State compatibility API permits hidden closure state; canonical Ψ contract is tested separately.", strict=True)
def test_current_transition_api_does_not_guarantee_x_r_sufficiency():
    """Red-team counterexample: a transition closure can depend on hidden state.

    This is intentionally an expected failure.  The current API accepts an
    arbitrary callable(State) -> State, so nothing in the type/contract stops
    the callable from closing over information outside State.
    """
    state_a = State(values={"x": 1, "relations": (("a", "b"),)})
    state_b = State(values={"x": 1, "relations": (("a", "b"),)})

    hidden = {"value": 0}

    def transition(state):
        return state.evolve(values={"x": state.values["x"] + hidden["value"]})

    result_a = Engine(transition).step(state_a)

    hidden["value"] = 100
    result_b = Engine(transition).step(state_b)

    # Same (X, R), different transition => current API does not enforce
    # E = E(X, R). This assertion is expected to fail until the kernel
    # contract eliminates hidden transition state.
    assert result_a.values["x"] == result_b.values["x"]


@pytest.mark.xfail(reason="Current transition API permits hidden closure state; kernel contract must eliminate this.", strict=True)
def test_kernel_contract_should_forbid_hidden_transition_dependency():
    """Contract target for the future minimal-state kernel."""
    state_a = State(values={"x": 1, "relations": (("a", "b"),)})
    state_b = State(values={"x": 1, "relations": (("a", "b"),)})

    hidden = {"value": 0}

    def transition(state):
        return state.evolve(values={"x": state.values["x"] + hidden["value"]})

    first = Engine(transition).step(state_a)
    hidden["value"] = 100
    second = Engine(transition).step(state_b)

    assert first.values["x"] == second.values["x"]
