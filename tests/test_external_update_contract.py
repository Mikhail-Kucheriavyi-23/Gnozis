from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_external_update_contract_exists():
    path = ROOT / "docs/EXTERNAL-WRITE-UPDATE-CONTRACT.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for term in (
        "update_id", "target_surface", "payload_digest", "authorization_scope",
        "provenance_id", "rollback_reference",
    ):
        assert term in text
