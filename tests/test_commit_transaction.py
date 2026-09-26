import pytest

from core.commit_transaction import commit_transaction
from core.history import AppendOnlyHistory, TransitionRecord


def rec(seq, prev, state):
    return TransitionRecord(seq, prev, state, "k1", state, True)


def test_prepare_rejects_non_next_sequence():
    history = AppendOnlyHistory().append(rec(0, "genesis", "s0"))
    with pytest.raises(ValueError, match="sequence"):
        commit_transaction(history, rec(2, "s0", "s2"), "current", "next")


def test_append_is_single_state_transition():
    history = AppendOnlyHistory()
    tx = commit_transaction(history, rec(0, "genesis", "s0"), "current", "next")
    appended = tx.append()

    assert len(history.records) == 0
    assert len(appended.records) == 1
    assert appended.head.state_hash == "s0"


def test_publish_requires_the_prepared_record_at_head():
    history = AppendOnlyHistory()
    tx = commit_transaction(history, rec(0, "genesis", "s0"), "current", "next")
    wrong = history.append(rec(0, "genesis", "other"))

    with pytest.raises(ValueError, match="prepared record"):
        tx.publish(wrong)


def test_publish_returns_new_value_only_after_append():
    history = AppendOnlyHistory()
    tx = commit_transaction(history, rec(0, "genesis", "s0"), "current", "next")

    result = tx.publish(tx.append())

    assert result.applied
    assert result.value == "next"
    assert result.history.head.state_hash == "s0"
