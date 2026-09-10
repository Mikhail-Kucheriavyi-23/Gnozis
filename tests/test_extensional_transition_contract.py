from core.contract import assert_extensional_transition
from core.state import State


def make_state(x, relations, metadata):
    values = {"x": x, "relations": relations}
    values.update(metadata)
    return State(values=values)


def test_valid_transition_is_extensional_over_x_and_r():
    def transition(state):
        return state.evolve(values={"x": state.values["x"] + len(state.values["relations"])})

    assert_extensional_transition(
        transition,
        make_state,
        3,
        (("a", "b"),),
    )


def test_hidden_closure_dependency_is_rejected():
    hidden = {"value": 0}

    def transition(state):
        return state.evolve(values={
            "x": state.values["x"] + hidden["value"],
            "relations": state.values["relations"],
        })

    def make_state_with_hidden(x, relations, metadata):
        hidden["value"] = metadata["hidden"]
        return make_state(x, relations, metadata)

    try:
        assert_extensional_transition(
            transition,
            make_state_with_hidden,
            3,
            (("a", "b"),),
        )
    except AssertionError:
        return

    raise AssertionError("transition with hidden closure state violated the Psi contract but was accepted")
