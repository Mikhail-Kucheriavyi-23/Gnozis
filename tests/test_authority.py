from core.authority import Evidence, foreign_evidence_is_non_authoritative

def test_foreign_evidence_cannot_authorize_execution():
    decision = foreign_evidence_is_non_authoritative(Evidence("external", {"ok": True}))
    assert not decision.admitted
    assert "cannot authorize" in decision.reason
