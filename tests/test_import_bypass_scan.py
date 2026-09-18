from tools.import_bypass_scan import scan

def test_no_forbidden_commit_imports_outside_canonical_chain():
    assert scan() == []
