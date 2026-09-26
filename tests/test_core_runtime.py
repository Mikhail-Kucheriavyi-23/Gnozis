from platform.core import AuditChain, Persistence, State, Transition, commit, recover


def test_commit_creates_next_state():
    source = State("s0", 0, {"x": 1})
    transition = Transition("t1", "s0", {"x": 2})
    result = commit(source, transition, accepted=True)
    assert result.state_id == "t1"
    assert result.version == 1
    assert result.value == {"x": 2}


def test_rejected_commit_fails_closed():
    source = State("s0", 0, {})
    transition = Transition("t1", "s0", {})
    try:
        commit(source, transition, accepted=False)
    except ValueError:
        return
    assert False, "rejected transition was committed"


def test_recovery_checks_digest():
    persistence = Persistence()
    state = State("s0", 0, {})
    persistence.save(state, "digest-1")
    assert recover(persistence, "s0", "digest-1") == state
    try:
        recover(persistence, "s0", "tampered")
    except ValueError:
        return
    assert False, "tampered state was recovered"


def test_audit_chain_links_records():
    chain = AuditChain()
    first = chain.append("op1", "commit", "d1")
    second = chain.append("op2", "commit", "d2")
    assert first.previous_digest == "GENESIS"
    assert second.previous_digest == "d1"
    assert chain.records() == (first, second)
