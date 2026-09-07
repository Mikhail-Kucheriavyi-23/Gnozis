import pytest

from bridge.psi_bridge import (
    CanonicalPointer,
    GnosisPsiBridge,
    JPsiWitness,
    PsiHalt,
    WitnessStatus,
)


def pointer(g, h, state_hash, finality_height=0, finality_hash=""):
    return CanonicalPointer(
        epoch=0,
        generation=g,
        height=h,
        state_hash=state_hash,
        finality_height=finality_height,
        finality_hash=finality_hash,
    )


def witness(old, new, status=WitnessStatus.DECIDED):
    return JPsiWitness(
        old=old,
        new=new,
        gamma_finality="gamma",
        omega="omega",
        token="token",
        status=status,
    )


def test_valid_decided_witness_is_installed_on_replay():
    old = pointer(0, 0, "h0")
    new = pointer(1, 1, "h1")
    bridge = GnosisPsiBridge(old)

    bridge.replay([witness(old, new)])

    assert bridge.canonical == new


def test_prepared_witness_is_aborted():
    old = pointer(0, 0, "h0")
    new = pointer(1, 1, "h1")
    bridge = GnosisPsiBridge(old)

    bridge.replay([witness(old, new, WitnessStatus.PREPARED)])

    assert bridge.canonical == old


def test_generation_reuse_halts():
    old = pointer(0, 0, "h0")
    conflicting = pointer(1, 1, "h1")
    bridge = GnosisPsiBridge(old)

    bad = JPsiWitness(
        old=old,
        new=conflicting,
        gamma_finality="gamma",
        omega="omega",
        token="token",
        status=WitnessStatus.DECIDED,
    )
    bad_new = pointer(2, 2, "h2")
    bad = JPsiWitness(
        old=replace_pointer_generation(bad.old, 5),
        new=bad_new,
        gamma_finality="gamma",
        omega="omega",
        token="token",
        status=WitnessStatus.DECIDED,
    )

    with pytest.raises(PsiHalt, match="generation gap"):
        bridge.replay([bad])


def replace_pointer_generation(p, generation):
    return CanonicalPointer(
        epoch=p.epoch,
        generation=generation,
        height=p.height,
        state_hash=p.state_hash,
        finality_height=p.finality_height,
        finality_hash=p.finality_hash,
    )


def test_conflicting_decisions_for_same_generation_halt():
    old = pointer(0, 0, "h0")
    a = pointer(1, 1, "ha")
    b = pointer(1, 1, "hb")
    bridge = GnosisPsiBridge(old)

    with pytest.raises(PsiHalt, match="conflicting durable witnesses"):
        bridge.replay([witness(old, a), witness(old, b)])


def test_finality_rollback_halts():
    old = pointer(0, 2, "h2", 2, "f2")
    new = pointer(1, 3, "h3", 1, "f1")
    bridge = GnosisPsiBridge(old)

    with pytest.raises(PsiHalt, match="invalid durable witness"):
        bridge.replay([witness(old, new)])


def test_same_generation_different_pointer_halts_on_install():
    current = pointer(1, 1, "h1")
    conflicting = pointer(1, 2, "h2")
    bridge = GnosisPsiBridge(current)

    with pytest.raises(PsiHalt, match="conflicting authority state"):
        bridge.install(conflicting)
