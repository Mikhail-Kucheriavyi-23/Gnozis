from dataclasses import FrozenInstanceError

from gnozis_core import AuditChain, Persistence, State, Transition, commit, recover
from gnozis_core.digest import state_digest


def test_commit_creates_next_state():
    source = State("s0", 0, {"x": 1})
    transition = Transition("t1", "s0", {"x": 2})
    result = commit(source, transition, accepted=True)
    assert result.state_id == "t1"
    assert result.version == 1
    assert result.value == {"x": 2}


def test_state_is_immutable():
    state = State("s0", 0, {})
    try:
        state.version = 1
    except FrozenInstanceError:
        return
    assert False, "state was mutable"


def test_rejected_commit_fails_closed():
    source = State("s0", 0, {})
    transition = Transition("t1", "s0", {})
    try:
        commit(source, transition, accepted=False)
    except ValueError:
        return
    assert False, "rejected transition was committed"


def test_wrong_transition_source_fails_closed():
    source = State("s0", 0, {})
    transition = Transition("t1", "other", {})
    try:
        commit(source, transition, accepted=True)
    except ValueError:
        return
    assert False, "foreign transition source was accepted"


def test_recovery_checks_digest():
    persistence = Persistence()
    state = State("s0", 0, {})
    persistence.save(state)
    assert recover(persistence, "s0", state_digest(state)) == state
    try:
        recover(persistence, "s0", "tampered")
    except ValueError:
        return
    assert False, "tampered state was recovered"


def test_persistence_detects_tampered_stored_digest():
    persistence = Persistence()
    state = State("s0", 0, {})
    stored = persistence.save(state)
    persistence._states["s0"] = type(stored)(state, "tampered")
    try:
        persistence.load("s0")
    except ValueError:
        return
    assert False, "tampered persisted record was accepted"


def test_digest_is_deterministic():
    a = State("s0", 1, {"b": 2, "a": 1})
    b = State("s0", 1, {"a": 1, "b": 2})
    assert state_digest(a) == state_digest(b)


def test_audit_chain_links_records():
    chain = AuditChain()
    first = chain.append("op1", "commit", "d1")
    second = chain.append("op2", "commit", "d2")
    assert first.previous_digest == "GENESIS"
    assert second.previous_digest == "d1"
    assert chain.records() == (first, second)
