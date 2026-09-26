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

    before = transition(make_state(3, (("a", "b"),), {}))
    hidden["value"] = 100
    after = transition(make_state(3, (("a", "b"),), {}))

    assert before != after, (
        "adversarial transition did not expose its hidden mutable dependency"
    )


from core.contract import assert_extensional_psi_transition
from core.psi_transition import PsiTransition
from core.state import Psi


def test_canonical_psi_transition_rejects_hidden_closure_dependency():
    hidden = {"value": 0}

    def transition(x, relations):
        return (x + hidden["value"], relations)

    operator = PsiTransition(transition)
    psi = Psi(1, (("a", "b"),))

    before = operator(psi)
    hidden["value"] = 100
    after = operator(psi)

    assert before != after, (
        "adversarial transition did not expose its hidden mutable dependency"
    )

    hidden["value"] = 0

    try:
        assert_extensional_psi_transition(
            operator,
            psi,
            lambda: hidden.update(value=100),
        )
    except AssertionError:
        return

    raise AssertionError(
        "extensionality helper accepted a transition with hidden mutable state"
    )
