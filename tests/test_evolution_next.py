from core import Engine, Relation, State, Uroboros


def test_uroboros_can_change_relations_endogenously():
    old_relation = Relation(source="hypothesis", target="test", relation_type="tested_by")
    new_relation = Relation(source="test", target="selection", relation_type="supports")

    def transition(state: State) -> State:
        return state.evolve(
            values={"score": state.values.get("score", 0) + 1},
            relations=(new_relation,),
        )

    core = Uroboros(
        state=State(values={"score": 0}, relations=(old_relation,)),
        engine=Engine(transition=transition),
        relations=(old_relation,),
    )

    evolved = core.step()

    assert evolved.state.relations == (new_relation,)
    assert evolved.relations == (new_relation,)
