from core.history import AppendOnlyHistory, TransitionRecord
from core.replay import replay
from core.state import Psi


def record(seq, prev, state):
    return TransitionRecord(seq, prev, state, "k1", f"c{seq}", True)


def test_replay_reconstructs_state_from_genesis_and_history():
    genesis = Psi(x=("a",), relations=())
    history = AppendOnlyHistory().append(record(0, "", "s0")).append(
        record(1, "s0", "s1")
    )

    def apply(state, record):
        return Psi(x=state.x + (record.state_hash,), relations=state.relations)

    result = replay(genesis, history, apply)
    assert result.applied == 2
    assert result.state.x == ("a", "s0", "s1")


def test_empty_history_returns_genesis():
    genesis = Psi(x=("g",), relations=())
    result = replay(genesis, AppendOnlyHistory(), lambda state, record: state)
    assert result.state == genesis
    assert result.applied == 0
