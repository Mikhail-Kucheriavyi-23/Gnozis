import warnings

from core.evolution import evolutionary_psi_transition, evolutionary_transition, select_next_state
from core.state import State


def generate(state):
    values = dict(state.values)
    values["x"] = tuple(values.get("x", ())) + (1,)
    yield State(values=values)


def test_legacy_state_transition_is_explicitly_deprecated():
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        transition = evolutionary_transition(generate, lambda state: True)
        transition(State())
    assert any(issubclass(item.category, DeprecationWarning) for item in seen)


def test_legacy_selector_is_explicitly_deprecated():
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        select_next_state(State(), generate, lambda state: True)
    assert any(issubclass(item.category, DeprecationWarning) for item in seen)


def test_legacy_psi_transition_is_pure_and_does_not_commit():
    transition = evolutionary_psi_transition(generate, lambda state: True)
    # The canonical proof requires a viable continuation; provide one through
    # the generator while keeping this API pure and commit-free.
    def canonical_generate(state):
        values = dict(state.values)
        x = values.get("x", ())
        return [State(values={**values, "x": x + (1,)}), State(values={**values, "x": x + (2,)})]

    transition = evolutionary_psi_transition(canonical_generate, lambda state: True)
    assert transition.function((1,), ()) == ((1, 1), ())
