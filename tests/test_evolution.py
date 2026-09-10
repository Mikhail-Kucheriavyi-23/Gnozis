from core import State, Uroboros, select_next_state


def test_generate_test_select_is_endogenous():
    initial = State(values={"score": 0})

    def generate(state):
        return [
            State(values={"score": 1}),
            State(values={"score": 2}),
            State(values={"score": -100}),
        ]

    def test(state):
        return state.values["score"] > 0

    result = select_next_state(initial, generate, test)
    assert result.values["score"] == 1


def test_no_external_selector_is_required():
    state = State(values={"score": 0})

    def generate(current):
        return [State(values={"score": current.values["score"] + 1})]

    def test(current):
        return current.values["score"] >= 0

    for _ in range(3):
        state = select_next_state(state, generate, test)

    assert state.values["score"] == 3


def test_uroboros_can_run_endogenous_generate_test_select():
    def generate(state):
        return [
            State(values={"score": state.values.get("score", 0) + 1}),
            State(values={"score": state.values.get("score", 0) - 1}),
        ]

    def test(state):
        return state.values["score"] >= 0

    core = Uroboros.evolutionary(
        generate=generate,
        test=test,
        state=State(values={"score": 0}),
    )

    evolved = core.step().step().step()
    assert evolved.state.values["score"] == 3
