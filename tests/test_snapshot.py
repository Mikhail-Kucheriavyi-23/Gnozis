from core.snapshot import Snapshot, SnapshotCertificate
from core.state import Psi


def test_snapshot_is_only_certified_by_history_head_state_and_kernel():
    state = Psi(x=("a",), relations=())
    snapshot = Snapshot(state, SnapshotCertificate("h1", "s1", "k2"))
    assert snapshot.is_cache_of("h1", "s1", "k2")
    assert not snapshot.is_cache_of("h0", "s1", "k2")
    assert not snapshot.is_cache_of("h1", "different", "k2")
    assert not snapshot.is_cache_of("h1", "s1", "k1")
