import pytest

from core.execution_contract import state_digest
from core.snapshot import Snapshot, SnapshotCertificate
from core.state import Psi


def snapshot_for(state, history_head="h1", kernel="k1"):
    return Snapshot(
        state=state,
        certificate=SnapshotCertificate(
            history_head=history_head,
            state_hash=state_digest(state),
            kernel_version=kernel,
        ),
    )


def test_snapshot_is_valid_only_for_matching_replay_result():
    state = Psi(x=("a",), relations=())
    snapshot = snapshot_for(state)

    assert snapshot.is_valid_for_replay(
        state,
        history_head="h1",
        kernel_version="k1",
    )


def test_snapshot_invalidates_when_replay_produces_different_state():
    state = Psi(x=("a",), relations=())
    replayed = Psi(x=("b",), relations=())
    snapshot = snapshot_for(state)

    assert not snapshot.is_valid_for_replay(
        replayed,
        history_head="h1",
        kernel_version="k1",
    )
    assert snapshot.invalidate_if_stale(
        replayed,
        history_head="h1",
        kernel_version="k1",
    ) is None


def test_snapshot_invalidates_when_history_head_changes():
    state = Psi(x=("a",), relations=())
    snapshot = snapshot_for(state, history_head="h1")

    assert snapshot.invalidate_if_stale(
        state,
        history_head="h2",
        kernel_version="k1",
    ) is None


def test_snapshot_invalidates_when_kernel_changes():
    state = Psi(x=("a",), relations=())
    snapshot = snapshot_for(state, kernel="k1")

    assert snapshot.invalidate_if_stale(
        state,
        history_head="h1",
        kernel_version="k2",
    ) is None


def test_snapshot_requires_canonical_replay_state():
    snapshot = snapshot_for(Psi(x=("a",), relations=()))
    with pytest.raises(TypeError):
        snapshot.is_valid_for_replay(
            ("not-psi",),
            history_head="h1",
            kernel_version="k1",
        )
