from core import Engine, Psi, make_psi_transition


def test_full_psi_cycle_generate_test_select_evolve_and_persist_shape():
    initial = Psi(("a",), (("a", "b"),))
    generated = [
        Psi(("a", "reject"), initial.relations),
        Psi(("a", "accept"), ()),
    ]

    def generate(psi):
        return generated

    def test(candidate):
        return candidate.x[-1] == "accept"

    transition = make_psi_transition(lambda x, relations: generated[1])
    result = Engine.from_psi(transition).step_psi(initial)

    assert result == generated[1]
    assert result.relations == ()
    assert isinstance(result, Psi)


def test_external_memory_or_web_is_not_part_of_fundamental_transition():
    initial = Psi(("a",), (("a", "b"),))
    external = {"memory": "noise", "web": "noise"}

    def transition(x, relations):
        return x + ("next",), relations

    engine = Engine.from_psi(make_psi_transition(transition))
    first = engine.step_psi(initial)
    external["web"] = "changed"
    second = engine.step_psi(initial)

    assert first == second
    assert first.x == ("a", "next")
