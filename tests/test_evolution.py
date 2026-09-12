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
            State(values={"x": state.values["x"] + 1, "relations": state.values["relations"]}),
            State(values={"x": state.values["x"] - 1, "relations": state.values["relations"]}),
        ]

    def test(state):
        return state.values["x"] >= 0

    core = Uroboros.evolutionary(
        generate=generate,
        test=test,
        state=State(values={"x": 0, "relations": ()}),
    )

    evolved = core.step().step().step()
    assert evolved.state.values["x"] == 3


def test_rule_set_can_evolve_with_the_state():
    initial = State(values={"x": 0, "relations": ()})

    def generate(state):
        return [
            State(values={"x": 1, "relations": ("r0", "r1")}),
            State(values={"x": 1, "relations": ("r0",)}),
        ]

    def test(state):
        return state.values["x"] > 0

    evolved = select_next_state(initial, generate, test)

    assert evolved.values["relations"] == ("r0",)
    assert initial.values["relations"] == ()


def test_uroboros_step_can_change_relations_without_external_correction():
    initial = State(values={"x": 0, "relations": ("r0",)})

    def generate(state):
        return [
            State(values={"x": state.values["x"] + 1,
                          "relations": state.values["relations"] + ("r1",)}),
        ]

    def test(state):
        return state.values["x"] > 0

    core = Uroboros.evolutionary(generate=generate, test=test, state=initial)
    evolved = core.step()

    assert evolved.state.values["relations"] == ("r0", "r1")
    assert core.state.values["relations"] == ("r0",)


def test_rule_change_is_derived_from_current_state_without_external_rule_updater():
    initial = State(values={"x": 0, "relations": ("r0",)})

    def generate(state):
        x = state.values["x"]
        relations = state.values["relations"]
        return [State(values={
            "x": x + 1,
            "relations": relations + (f"r{x + 1}",),
        })]

    def test(state):
        return state.values["x"] > 0

    core = Uroboros.evolutionary(generate=generate, test=test, state=initial)
    evolved = core.step()

    assert evolved.state.values["x"] == 1
    assert evolved.state.values["relations"] == ("r0", "r1")
    assert core.state.values["relations"] == ("r0",)
