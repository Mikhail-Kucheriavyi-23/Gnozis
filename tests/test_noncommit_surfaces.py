import pytest

from core.branch import Branch
from core.history import AppendOnlyHistory
from core.merge import merge
from core.psi_transition import PsiTransition
from core.refinement import refine
from core.replay import replay
from core.snapshot import Snapshot, SnapshotCertificate
from core.state import Psi


def test_merge_conflict_does_not_produce_candidate():
    a = Branch(psi=Psi(x=(1,), relations=()))
    b = Branch(psi=Psi(x=(2,), relations=()))
    result = merge(a, b)
    assert result.candidate is None
    assert not result.compatible


def test_refinement_only_witnesses_transitions():
    t = PsiTransition(lambda x, r: (x, r))
    proof = refine(t, t, lambda a, b: a == b, [Psi(x=(), relations=())])
    assert proof.holds() is True


def test_snapshot_is_only_cache_observation():
    psi = Psi(x=(), relations=())
    snap = Snapshot(
        state=psi,
        certificate=SnapshotCertificate(
            history_head="h",
            state_hash="s",
            kernel_version="k",
        ),
    )
    assert snap.is_cache_of("h", "s", "k")


def test_replay_requires_explicit_transition_applier():
    history = AppendOnlyHistory()
    with pytest.raises(TypeError):
        replay(Psi(x=(), relations=()), history, None)
