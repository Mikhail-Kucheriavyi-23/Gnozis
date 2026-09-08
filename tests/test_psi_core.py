from dataclasses import FrozenInstanceError

import pytest

from core import Engine, Relation, State, Uroboros, select_next_state


def test_state_owns_x_and_r_without_aliasing_relation_container():
    relation = Relation(source="a", target="b")
    relations = [relation]
    state = State(values={"x": 1}, relations=relations)

    relations.append(Relation(source="b", target="c"))

    assert state.values["x"] == 1
    assert state.relations == (relation,)


def test_evolve_values_preserves_r_and_old_state():
    relation = Relation(source="a", target="b")
    state = State(values={"x": 1}, relations=(relation,))

    evolved = state.evolve(values={"x": 2})

    assert evolved.values["x"] == 2
    assert evolved.relations == state.relations
    assert state.values["x"] == 1
    assert state.relations == (relation,)
    assert evolved is not state


def test_evolve_relations_preserves_x():
    old_relation = Relation(source="a", target="b")
    new_relation = Relation(source="b", target="c")
    state = State(values={"x": 1}, relations=(old_relation,))

    evolved = state.evolve(relations=(new_relation,))

    assert evolved.values == state.values
    assert evolved.relations == (new_relation,)
    assert state.relations == (old_relation,)


def test_evolve_values_and_relations_together():
    old_relation = Relation(source="a", target="b")
    new_relation = Relation(source="b", target="c")
    state = State(values={"x": 1}, relations=(old_relation,))

    evolved = state.evolve(values={"x": 2}, relations=(new_relation,))

    assert evolved.values["x"] == 2
    assert evolved.relations == (new_relation,)
    assert state.values["x"] == 1
    assert state.relations == (old_relation,)


def test_evolve_relations_empty_is_explicit_empty_r():
    relation = Relation(source="a", target="b")
    state = State(values={"x": 1}, relations=(relation,))

    evolved = state.evolve(relations=())

    assert evolved.relations == ()
    assert len(evolved.relations) == 0
    assert state.relations == (relation,)


def test_evolve_relations_none_is_rejected_not_treated_as_omitted_or_empty():
    state = State(values={"x": 1})

    with pytest.raises(TypeError):
        state.evolve(relations=None)


def test_evolve_values_none_is_rejected_not_treated_as_omitted():
    state = State(values={"x": 1})

    with pytest.raises(TypeError):
        state.evolve(values=None)


def test_evolve_requires_an_explicit_component():
    state = State(values={"x": 1})

    with pytest.raises(TypeError):
        state.evolve()  # type: ignore[call-arg]


def test_state_rejects_non_mapping_values():
    with pytest.raises(TypeError):
        State(values=[("x", 1)])  # type: ignore[arg-type]


def test_state_rejects_non_relation_members():
    with pytest.raises(TypeError):
        State(values={"x": 1}, relations=("not-a-relation",))  # type: ignore[arg-type]


def test_state_outer_mapping_and_nested_standard_containers_are_protected():
    source = {"nested": {"items": [1, 2]}}
    state = State(values=source)

    source["nested"]["items"].append(3)
    source["nested"]["new"] = True

    assert state.values["nested"]["items"] == [1, 2]
    assert "new" not in state.values["nested"]

    with pytest.raises(TypeError):
        state.values["nested"] = {}  # type: ignore[index]

    with pytest.raises(TypeError):
        state.values["nested"]["items"].append(3)


def test_state_outer_assignment_is_rejected():
    state = State(values={"x": 1})

    with pytest.raises(FrozenInstanceError):
        state.values = {"x": 2}  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        state.relations = ()  # type: ignore[misc]


def test_state_values_remain_json_compatible_for_standard_dict_list_data():
    import json

    state = State(values={"nested": {"items": [1, 2]}})

    assert json.dumps(state.values) == '{"nested": {"items": [1, 2]}}'


def test_relation_outer_object_is_frozen_but_arbitrary_endpoint_semantics_are_unchanged():
    relation = Relation(source="a", target="b")

    with pytest.raises(FrozenInstanceError):
        relation.source = "changed"  # type: ignore[misc]


def test_uroboros_with_relations_stores_r_in_state():
    relation = Relation(source="a", target="b")
    core = Uroboros().with_relations((relation,))

    assert core.state.relations == (relation,)


def test_evolution_can_change_r_as_part_of_complete_state():
    relation_a = Relation(source="a", target="b")
    relation_b = Relation(source="b", target="c")
    initial = State(values={"step": 0}, relations=(relation_a,))

    def generate(state):
        return [
            State(
                values={"step": state.values["step"] + 1},
                relations=(relation_b,),
            )
        ]

    def test(state):
        return True

    def select(valid):
        return valid[0]

    core = Uroboros.evolutionary(
        generate=generate,
        test=test,
        select=select,
        state=initial,
    )
    evolved = core.run(2)

    assert evolved.state.values["step"] == 2
    assert evolved.state.relations == (relation_b,)
    assert initial.relations == (relation_a,)


def test_gts_rejects_non_bool_tester_result():
    state = State(values={"score": 0})
    candidate = State(values={"score": 1})

    with pytest.raises(TypeError, match="Tester must return a bool"):
        select_next_state(
            state,
            generate=lambda _: [candidate],
            test=lambda _: 1,  # type: ignore[return-value]
            select=lambda valid: valid[0],
        )


def test_gts_rejects_non_state_generator_output():
    state = State(values={"score": 0})

    with pytest.raises(TypeError, match="Generator must produce State instances"):
        select_next_state(
            state,
            generate=lambda _: [object()],  # type: ignore[list-item]
            test=lambda _: True,
            select=lambda valid: valid[0],
        )


def test_gts_accepts_value_equal_tested_state():
    state = State(values={"score": 0})
    candidate = State(values={"score": 1})
    equal_but_distinct = State(values={"score": 1})

    result = select_next_state(
        state,
        generate=lambda _: [candidate],
        test=lambda _: True,
        select=lambda valid: equal_but_distinct,
    )

    assert result == candidate
    assert result is equal_but_distinct


def test_gts_rejects_non_state_initial_input():
    with pytest.raises(TypeError, match="state must be a State instance"):
        select_next_state(
            object(),  # type: ignore[arg-type]
            generate=lambda _: [],
            test=lambda _: True,
            select=lambda valid: valid[0],
        )


def test_gts_rejects_non_callable_operators():
    state = State(values={"score": 0})

    with pytest.raises(TypeError, match="generate must be callable"):
        select_next_state(state, None, lambda _: True, lambda valid: valid[0])  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="test must be callable"):
        select_next_state(state, lambda _: [state], None, lambda valid: valid[0])  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="select must be callable"):
        select_next_state(state, lambda _: [state], lambda _: True, None)  # type: ignore[arg-type]


def test_default_state_has_empty_relation_structure():
    state = State()

    assert state.relations == ()


def test_engine_rejects_non_callable_transition():
    with pytest.raises(TypeError, match="transition must be callable"):
        Engine(transition=None)  # type: ignore[arg-type]


def test_engine_rejects_non_state_input():
    engine = Engine(transition=lambda state: state)

    with pytest.raises(TypeError, match="requires a State instance"):
        engine.step(object())  # type: ignore[arg-type]


def test_state_rejects_cyclic_standard_containers():
    cyclic = []
    cyclic.append(cyclic)

    with pytest.raises(ValueError, match="cyclic standard container"):
        State(values={"cycle": cyclic})
