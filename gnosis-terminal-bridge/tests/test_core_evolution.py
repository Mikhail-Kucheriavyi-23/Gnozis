from core import State

from src.agency_context import AgencyContext, AgencyIdentity
from src.core_evolution import engine_from_agency_context
from core import Uroboros


def make_context():
    return AgencyContext(
        identity=AgencyIdentity(
            provider="github",
            subject="Mikhail-Kucheriavyi-23",
            authenticated=True,
        ),
        epoch=1,
        generation=2,
        height=3,
        expires_at=9999999999,
    )


def test_agency_context_is_available_to_transition_and_evolution_needs_no_external_call():
    context = make_context()
    calls = []

    def transition(state, agency_context):
        calls.append(agency_context.identity.subject)
        return state.evolve(
            agency_seen=agency_context.identity.subject,
            next_height=agency_context.height + 1,
        )

    engine = engine_from_agency_context(context, transition)
    initial = State(values={"value": 10})
    uroboros = Uroboros(state=initial, engine=engine)

    evolved = uroboros.step()

    assert evolved.state.values["value"] == 10
    assert evolved.state.values["agency_seen"] == "Mikhail-Kucheriavyi-23"
    assert evolved.state.values["next_height"] == 4
    assert calls == ["Mikhail-Kucheriavyi-23"]

    # The second step uses only State -> State; no new identity lookup occurs.
    evolved_again = evolved.step()
    assert evolved_again.state.values["agency_seen"] == "Mikhail-Kucheriavyi-23"
    assert calls == ["Mikhail-Kucheriavyi-23", "Mikhail-Kucheriavyi-23"]


def test_same_state_and_same_agency_context_are_deterministic():
    context = make_context()

    def transition(state, agency_context):
        return state.evolve(
            subject=agency_context.identity.subject,
            height=agency_context.height,
        )

    engine = engine_from_agency_context(context, transition)
    initial = State(values={"seed": 7})

    first = engine.step(initial)
    second = engine.step(initial)

    assert first == second


def test_unauthenticated_context_cannot_create_evolution_engine():
    context = AgencyContext(
        identity=AgencyIdentity(
            provider="github",
            subject="untrusted",
            authenticated=False,
        ),
        epoch=1,
        generation=2,
        height=3,
        expires_at=9999999999,
    )

    def transition(state, agency_context):
        return state

    try:
        engine_from_agency_context(context, transition)
    except ValueError as exc:
        assert str(exc) == "Agency identity is not authenticated"
    else:
        raise AssertionError("Unauthenticated context must be rejected")
