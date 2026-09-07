from core import State

from src.autonomous_selection import select_next_state


def test_generate_test_select_chooses_valid_best_candidate():
    initial = State(values={"score": 0})

    def generate(state):
        return [
            State(values={"score": state.values["score"] + 1}),
            State(values={"score": state.values["score"] + 3}),
            State(values={"score": -1}),
        ]

    def test(state):
        return state.values["score"] >= 1

    def select(candidates):
        return max(candidates, key=lambda candidate: candidate.values["score"])

    result = select_next_state(initial, generate, test, select)

    assert result.values == {"score": 3}


def test_selection_is_internal_and_does_not_require_external_operator():
    initial = State(values={"score": 4})
    calls = []

    def generate(state):
        calls.append("generate")
        return [
            State(values={"score": state.values["score"] + 2}),
            State(values={"score": state.values["score"] + 5}),
        ]

    def test(state):
        calls.append(("test", state.values["score"]))
        return state.values["score"] <= 9

    def select(candidates):
        calls.append("select")
        return candidates[0]

    result = select_next_state(initial, generate, test, select)

    assert result.values == {"score": 6}
    assert calls == ["generate", ("test", 6), ("test", 9), "select"]


def test_invalid_selection_cannot_escape_test_filter():
    initial = State(values={"score": 0})

    def generate(state):
        return [State(values={"score": 2})]

    def test(state):
        return True

    def select(candidates):
        return State(values={"score": 99})

    try:
        select_next_state(initial, generate, test, select)
    except ValueError as error:
        assert str(error) == "Selector must choose one of the tested candidates"
    else:
        raise AssertionError("An untested selected state must be rejected")
