from core import State
from core.evolution import evolutionary_psi_transition, select_next_state


def test_generic_selection_does_not_require_psi_fields():
    initial = State(values={"score": 0})

    def generate(_state):
        return [State(values={"score": 2}), State(values={"score": 1})]

    def test(_state):
        return True

    result = select_next_state(initial, generate, test)
    assert result.values["score"] == 1


def test_canonical_psi_selection_requires_x_and_relations():
    def generate(_state):
        return [
            State(values={"x": 1, "relations": ("r",)}),
            State(values={"x": 2, "relations": ("r",)}),
        ]

    def test(_state):
        return True

    transition = evolutionary_psi_transition(generate, test)
    result = transition(State(values={"x": 0, "relations": ()}).to_psi())

    assert result.x == 1
    assert result.relations == ("r",)
