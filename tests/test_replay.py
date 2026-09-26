import pytest

from core.execution_contract import state_digest
from core.history import AppendOnlyHistory, TransitionRecord
from core.replay import replay
from core.state import Psi


def make_record(sequence, previous_hash, state):
    digest = state_digest(state)
    return TransitionRecord(
        sequence=sequence,
        previous_hash=previous_hash,
        state_hash=digest,
        kernel_version="k1",
        candidate_hash=digest,
        admitted=True,
    )


def test_replay_reconstructs_state_with_hash_bound_records():
    genesis = Psi(x=("a",), relations=())
    state0 = Psi(x=("a", "s0"), relations=())
    state1 = Psi(x=("a", "s0", "s1"), relations=())
    history = AppendOnlyHistory().append(
        make_record(0, "genesis", state0)
    ).append(
        make_record(1, state_digest(state0), state1)
    )

    def apply(state, record):
        if record.sequence == 0:
            return state0
        return state1

    result = replay(genesis, history, apply)
    assert result.applied == 2
    assert result.state == state1


def test_empty_history_returns_genesis():
    genesis = Psi(x=("g",), relations=())
    result = replay(genesis, AppendOnlyHistory(), lambda state, record: state)
    assert result.state == genesis
    assert result.applied == 0


def test_replay_requires_explicit_applier():
    genesis = Psi(x=("g",), relations=())
    with pytest.raises(TypeError):
        replay(genesis, AppendOnlyHistory(), None)


def test_replay_rejects_state_substitution():
    genesis = Psi(x=("g",), relations=())
    state0 = Psi(x=("g", "s0"), relations=())
    substituted = Psi(x=("g", "wrong"), relations=())
    history = AppendOnlyHistory().append(
        make_record(0, "genesis", state0)
    )
    calls = []

    def apply(state, record):
        calls.append(state)
        return substituted

    with pytest.raises(ValueError, match="state_hash"):
        replay(genesis, history, apply)

    assert len(calls) == 1


def test_replay_rejects_previous_state_substitution_before_second_apply():
    genesis = Psi(x=("g",), relations=())
    state0 = Psi(x=("g", "s0"), relations=())
    state1 = Psi(x=("g", "s1"), relations=())
    history = AppendOnlyHistory().append(
        make_record(0, "genesis", state0)
    ).append(
        make_record(1, state_digest(state0), state1)
    )
    calls = []

    def apply(state, record):
        calls.append(record.sequence)
        if record.sequence == 0:
            return state0
        return state1

    # A tampered first application is rejected at record 0, so record 1
    # can never consume a substituted state.
    tampered_history = AppendOnlyHistory(
        records=(
            history.records[0],
            TransitionRecord(
                sequence=1,
                previous_hash=state_digest(Psi(x=("g", "tampered"), relations=())),
                state_hash=state_digest(state1),
                kernel_version="k1",
                candidate_hash=state_digest(state1),
                admitted=True,
            ),
        )
    )

    with pytest.raises(ValueError, match="previous_hash"):
        replay(genesis, tampered_history, apply)

    assert calls == [0]
