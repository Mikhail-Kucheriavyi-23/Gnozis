from dataclasses import FrozenInstanceError

import pytest

from core import Relation, State, Uroboros


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


def test_evolve_requires_an_explicit_component():
    state = State(values={"x": 1})

    with pytest.raises(TypeError):
        state.evolve()  # type: ignore[call-arg]


def test_state_outer_mapping_and_nested_standard_containers_are_protected():
    source = {"nested": {"items": [1, 2]}}
    state = State(values=source)

    source["nested"]["items"].append(3)
    source["nested"]["new"] = True

    assert state.values["nested"]["items"] == (1, 2)
    assert "new" not in state.values["nested"]

    with pytest.raises(TypeError):
        state.values["nested"] = {}  # type: ignore[index]


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
            State(values={"step": state.values["step"] + 1}, relations=(relation_b,))
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
