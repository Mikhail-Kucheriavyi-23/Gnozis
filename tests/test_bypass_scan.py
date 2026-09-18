from tools.bypass_scan import scan

def test_no_direct_commit_bypass_in_core():
    findings = scan()
    assert findings == []
