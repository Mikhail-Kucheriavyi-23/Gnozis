import pytest

from core.root_invariant import RootInvariant, preserve_root


def test_k0_holds_before_and_after():
    k0 = RootInvariant(lambda kernel: kernel.get("sealed") is True)
    before = {"sealed": True}
    after = {"sealed": True, "version": 2}
    assert preserve_root(k0, before, after)


def test_k0_rejects_root_break():
    k0 = RootInvariant(lambda kernel: kernel.get("sealed") is True)
    with pytest.raises(ValueError, match="K0"):
        k0.require({"sealed": False})


def test_k0_fails_if_before_state_was_invalid():
    k0 = RootInvariant(lambda kernel: kernel.get("sealed") is True)
    assert not preserve_root(k0, {"sealed": False}, {"sealed": True})
