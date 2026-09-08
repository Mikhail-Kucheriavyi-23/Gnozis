from core import State, select_next_state


def test_generate_test_select_selects_only_tested_candidates():
    initial = State(values={"score": 0})

    def generate(state):
        return [
            State(values={"score": state.values["score"] + 1}),
            State(values={"score": state.values["score"] + 2}),
            State(values={"score": -100}),
        ]

    def test(state):
        return state.values["score"] > 0

    def select(valid):
        return max(valid, key=lambda state: state.values["score"])

    result = select_next_state(initial, generate, test, select)

    assert result.values["score"] == 2


def test_generate_test_select_rejects_untested_selection():
    initial = State(values={"score": 0})
    rejected = State(values={"score": -1})
    accepted = State(values={"score": 1})

    def generate(state):
        return [accepted, rejected]

    def test(state):
        return state.values["score"] > 0

    def select(valid):
        return rejected

    try:
        select_next_state(initial, generate, test, select)
    except ValueError as error:
        assert str(error) == "Selector must choose one of the tested candidates"
    else:
        raise AssertionError("untested candidate was selected")


def test_evolution_can_continue_without_external_selection_step():
    state = State(values={"score": 0})

    def generate(current):
        return [State(values={"score": current.values["score"] + 1})]

    def test(current):
        return current.values["score"] >= 0

    def select(valid):
        return valid[0]

    for _ in range(3):
        state = select_next_state(state, generate, test, select)

    assert state.values["score"] == 3
