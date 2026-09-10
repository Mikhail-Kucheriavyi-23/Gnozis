from core import Engine, Psi, make_psi_transition


def test_relation_set_can_expand_endogenously():
    psi = Psi(("a", "b"), (("a", "b"),))

    engine = Engine.from_psi(
        make_psi_transition(
            lambda x, relations: (x + ("c",), relations + (("b", "c"),))
        )
    )

    result = engine.step_psi(psi)

    assert result.relations == (("a", "b"), ("b", "c"))


def test_relation_set_can_contract_endogenously():
    psi = Psi(("a", "b", "c"), (("a", "b"), ("b", "c")))

    engine = Engine.from_psi(
        make_psi_transition(lambda x, relations: (x, (relations[0],)))
    )

    result = engine.step_psi(psi)

    assert result.relations == (("a", "b"),)


def test_relation_set_can_become_empty_without_external_selector():
    psi = Psi(("a", "b"), (("a", "b"),))

    engine = Engine.from_psi(make_psi_transition(lambda x, relations: (x, ())))
    result = engine.step_psi(psi)

    assert result.relations == ()
