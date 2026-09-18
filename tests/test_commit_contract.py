import pytest
from core.commit_contract import commit_once
from core.history import AppendOnlyHistory, TransitionRecord

def rec(seq, prev, state):
    return TransitionRecord(seq, prev, state, "k1", f"c{seq}", True)

def test_commit_is_idempotent_for_same_head():
    h = AppendOnlyHistory().append(rec(0, "", "s0"))
    result = commit_once(h, rec(0, "", "s0"), "current", "new")
    assert not result.applied
    assert result.value == "current"
    assert result.history == h

def test_commit_rejects_conflicting_same_sequence():
    h = AppendOnlyHistory().append(rec(0, "", "s0"))
    with pytest.raises(ValueError, match="conflicts"):
        commit_once(h, rec(0, "", "other"), "current", "new")

def test_commit_accepts_next_sequence():
    h = AppendOnlyHistory().append(rec(0, "", "s0"))
    result = commit_once(h, rec(1, "s0", "s1"), "current", "next")
    assert result.applied
    assert result.value == "next"
    assert result.history.head.state_hash == "s1"
