from core import Relation, State, Uroboros, select_next_state


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


def test_selector_cannot_replace_tested_candidate_with_equal_copy():
    initial = State(values={"score": 0})
    accepted = State(values={"score": 1})

    def generate(state):
        return [accepted]

    def test(state):
        return True

    def select(valid):
        return State(values={"score": 1})

    try:
        select_next_state(initial, generate, test, select)
    except ValueError as error:
        assert str(error) == "Selector must choose one of the tested candidates"
    else:
        raise AssertionError("selector returned a non-lineage copy")


def test_generator_cannot_inject_non_state_candidate():
    initial = State(values={"score": 0})

    def generate(state):
        return [State(values={"score": 1}), {"score": 2}]

    def test(state):
        return True

    def select(valid):
        return valid[0]

    try:
        select_next_state(initial, generate, test, select)
    except TypeError as error:
        assert str(error) == "Generator must produce only State candidates"
    else:
        raise AssertionError("non-State candidate crossed the generation boundary")


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


def test_uroboros_can_run_endogenous_generate_test_select():
    def generate(state):
        return [
            State(values={"score": state.values.get("score", 0) + 1}),
            State(values={"score": state.values.get("score", 0) - 1}),
        ]

    def test(state):
        return state.values["score"] >= 0

    def select(valid):
        return max(valid, key=lambda state: state.values["score"])

    core = Uroboros.evolutionary(
        generate=generate,
        test=test,
        select=select,
        state=State(values={"score": 0}),
    )

    evolved = core.step().step().step()
    assert evolved.state.values["score"] == 3


def test_uroboros_evolution_preserves_relations_when_candidate_uses_state_evolve():
    relation = Relation(
        source="hypothesis",
        target="test",
        relation_type="tested_by",
    )

    def generate(state):
        return [
            state.evolve(
                values={"score": state.values.get("score", 0) + 1}
            )
        ]

    def test(state):
        return state.values["score"] >= 0

    def select(valid):
        return valid[0]

    core = Uroboros.evolutionary(
        generate=generate,
        test=test,
        select=select,
        state=State(values={"score": 0}, relations=(relation,)),
    )

    evolved = core.step()

    assert evolved.state.values["score"] == 1
    assert evolved.state.relations == (relation,)
    assert evolved.relations == (relation,)


def test_uroboros_evolution_can_explicitly_remove_relations():
    relation = Relation(
        source="hypothesis",
        target="test",
        relation_type="tested_by",
    )

    def generate(state):
        return [state.evolve(values=state.values, relations=())]

    def test(state):
        return True

    def select(valid):
        return valid[0]

    core = Uroboros.evolutionary(
        generate=generate,
        test=test,
        select=select,
        state=State(values={"score": 0}, relations=(relation,)),
    )

    evolved = core.step()

    assert evolved.state.relations == ()
    assert evolved.relations == ()
