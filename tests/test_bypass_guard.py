from core.bypass_guard import canonical_entrypoint, forbidden_direct_commit_symbols

def test_canonical_entrypoint_is_explicit():
    assert canonical_entrypoint() == "core.canonical_chain.admit_transition"

def test_direct_commit_symbols_are_audit_targets():
    assert "AppendOnlyHistory.append" in forbidden_direct_commit_symbols()
    assert "commit_once" in forbidden_direct_commit_symbols()
