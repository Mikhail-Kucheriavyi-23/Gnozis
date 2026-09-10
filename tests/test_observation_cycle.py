from datetime import datetime, timezone

import pytest

from core.memory import InMemoryStore
from core.observation import Observation
from core.observation_cycle import ObservationCycle
from core.state import Psi


def obs(value):
    return Observation(
        source="test",
        payload=value,
        observed_at=datetime.now(timezone.utc),
    )


def test_accepted_observation_produces_candidate_and_is_remembered():
    memory = InMemoryStore()
    current = Psi(x={"n": 0}, relations=())

    cycle = ObservationCycle(
        memory=memory,
        build_candidate=lambda psi, observation: Psi(
            x={"n": observation.payload}, relations=psi.relations
        ),
        test_candidate=lambda psi, candidate, observation: candidate.x["n"] > psi.x["n"],
    )

    nxt = cycle.ingest(current, obs(1))

    assert nxt.x["n"] == 1
    assert memory.recall(limit=1)[0].payload == 1


def test_rejected_observation_cannot_change_psi():
    memory = InMemoryStore()
    current = Psi(x={"n": 5}, relations=())
    cycle = ObservationCycle(
        memory=memory,
        build_candidate=lambda psi, observation: Psi(x={"n": observation.payload}, relations=()),
        test_candidate=lambda psi, candidate, observation: False,
    )

    nxt = cycle.ingest(current, obs(1))

    assert nxt == current
    assert memory.recall(limit=1)[0].payload == 1


def test_candidate_test_must_return_real_bool():
    cycle = ObservationCycle(
        memory=InMemoryStore(),
        build_candidate=lambda psi, observation: psi,
        test_candidate=lambda psi, candidate, observation: 1,
    )

    with pytest.raises(TypeError):
        cycle.ingest(Psi(x={}, relations=()), obs(None))
