from core import Engine, Psi, make_psi_transition


def test_engine_accepts_and_returns_only_psi_at_fundamental_boundary():
    psi = Psi(("a", "b"), (("a", "b"),))

    transition = make_psi_transition(
        lambda x, relations: (x + ("c",), relations + (("b", "c"),))
    )
    result = Engine.from_psi(transition).step_psi(psi)

    assert isinstance(result, Psi)
    assert result.x == ("a", "b", "c")
    assert result.relations == (("a", "b"), ("b", "c"))


def test_relation_set_can_evolve_to_empty():
    psi = Psi(("a",), (("a", "b"),))
    transition = make_psi_transition(lambda x, relations: (x, ()))

    result = Engine.from_psi(transition).step_psi(psi)

    assert result.relations == ()


def test_same_psi_and_same_transition_are_reproducible():
    psi = Psi((1,), ((1, 1),))
    transition = make_psi_transition(
        lambda x, relations: (x + (len(relations),), relations)
    )
    engine = Engine.from_psi(transition)

    assert engine.step_psi(psi) == engine.step_psi(psi)


def test_transition_receives_no_state_wrapper():
    observed = []
    psi = Psi(("x",), ())

    def transition(x, relations):
        observed.append((type(x), type(relations)))
        return x, relations

    Engine.from_psi(make_psi_transition(transition)).step_psi(psi)

    assert observed == [(tuple, tuple)]
