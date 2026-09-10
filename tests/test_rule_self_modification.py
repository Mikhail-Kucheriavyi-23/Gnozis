from core import Engine, Psi, make_psi_transition


def test_psi_can_carry_and_change_its_internal_rule_without_external_selector():
    initial = Psi(
        ("x",),
        (("rule", "append"),),
    )

    def transition(x, relations):
        rules = dict(relations)
        if rules["rule"] == "append":
            return x + ("y",), (("rule", "drop"),)
        return x, relations

    engine = Engine.from_psi(make_psi_transition(transition))
    evolved = engine.step_psi(initial)

    assert evolved.x == ("x", "y")
    assert evolved.relations == (("rule", "drop"),)


def test_changed_rule_controls_the_following_transition():
    initial = Psi((0,), (("rule", "increment"),))

    def transition(x, relations):
        rule = dict(relations)["rule"]
        if rule == "increment":
            return x + (x[-1] + 1,), (("rule", "freeze"),)
        return x, relations

    engine = Engine.from_psi(make_psi_transition(transition))
    first = engine.step_psi(initial)
    second = engine.step_psi(first)

    assert first.x == (0, 1)
    assert first.relations == (("rule", "freeze"),)
    assert second == first


def test_rule_change_is_part_of_psi_not_external_mutable_selector():
    initial = Psi((0,), (("rule", "increment"),))
    external_selector = {"rule": "corrupt"}

    def transition(x, relations):
        rule = dict(relations)["rule"]
        if rule == "increment":
            return x + (1,), (("rule", "freeze"),)
        return x, relations

    engine = Engine.from_psi(make_psi_transition(transition))
    result_a = engine.step_psi(initial)
    external_selector["rule"] = "increment"
    result_b = engine.step_psi(initial)

    assert result_a == result_b
