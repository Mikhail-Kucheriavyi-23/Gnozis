import pytest

from core.history import AppendOnlyHistory, TransitionRecord


def rec(seq, prev, state, kernel="k1"):
    return TransitionRecord(seq, prev, state, kernel, f"c{seq}", True, f"e{seq}")


def test_history_is_chained_and_append_only():
    history = AppendOnlyHistory().append(rec(0, "", "s0"))
    history = history.append(rec(1, "s0", "s1"))
    assert [r.state_hash for r in history.records] == ["s0", "s1"]


def test_history_rejects_broken_chain():
    history = AppendOnlyHistory().append(rec(0, "", "s0"))
    with pytest.raises(ValueError, match="chain"):
        history.append(rec(1, "wrong", "s1"))


def test_history_rejects_unaccepted_transition():
    with pytest.raises(ValueError, match="accepted"):
        TransitionRecord(0, "", "s0", "k1", "c0", False)


def test_history_rejects_tampered_previous_hash_on_append():
    history = AppendOnlyHistory().append(rec(0, "", "s0"))
    tampered = rec(1, "s0-tampered", "s1")
    with pytest.raises(ValueError, match="chain"):
        history.append(tampered)


def test_history_rejects_sequence_tampering():
    history = AppendOnlyHistory().append(rec(0, "", "s0"))
    with pytest.raises(ValueError, match="sequence"):
        history.append(rec(2, "s0", "s2"))
