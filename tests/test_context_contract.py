from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_context_contract_exists():
    path = ROOT / "docs/CONTEXT-CONTINUITY-CONTRACT.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for term in ("Identity", "Project", "Task", "Knowledge", "Session", "Provenance"):
        assert term in text


def test_provenance_contract_exists():
    path = ROOT / "docs/PROVENANCE-CONTRACT.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for term in ("provenance_id", "source_reference", "content_digest", "schema_version"):
        assert term in text
